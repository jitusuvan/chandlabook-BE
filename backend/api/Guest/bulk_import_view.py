from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

import csv
from io import StringIO
from decimal import Decimal
from datetime import datetime
from django.db import transaction

def parse_flexible_date(date_str):
    """Support YYYY-MM-DD, DD-MM-YYYY, DD-MM-YY"""
    for fmt in ['%Y-%m-%d', '%d-%m-%Y', '%d-%m-%y']:
        try:
            return datetime.strptime(date_str, fmt).date()
        except ValueError:
            continue
    raise ValueError(f"Invalid date '{date_str}'. Expected: YYYY-MM-DD, DD-MM-YYYY, or DD-MM-YY")

from api.Guest.model import Guest
from api.GuestRecord.model import GuestRecord
from api.Event.model import Event


class BulkGuestImportWithRecordsView(APIView):
    parser_classes = [MultiPartParser, FormParser]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        file_obj = request.FILES.get('file')

        if not file_obj:
            return Response({'error': 'File required'}, status=400)

        user = request.user

        content = file_obj.read().decode('utf-8')
        reader = csv.DictReader(StringIO(content))
        rows = list(reader)

        # ✅ Header validation
        required_fields = [
            'first_name','last_name','surname','mobile_no','city',
            'event_name','date','amount','select','event_type','bride_groom','pay_later'
        ]

        if not rows or not all(field in rows[0] for field in required_fields):
            return Response({'error': f'Invalid CSV header. Required: {required_fields}'}, status=400)

        guest_new = 0
        record_new = 0
        errors = []

        with transaction.atomic():
            for index, row in enumerate(rows, start=1):
                try:
                    # ✅ Guest (reuse if exists)
                    guest, created = Guest.objects.get_or_create(
                        mobile_no=row['mobile_no'],
                        defaults={
                            'user': user,
                            'first_name': row['first_name'],
                            'last_name': row.get('last_name', ''),
                            'surname': row.get('surname', ''),
                            'city': row['city']
                        }
                    )
                    if created:
                        guest_new += 1

                    # Parse date first
                    event_date = parse_flexible_date(row['date'])

                    if row['select'] == 'mukel':
                        # No event created, record without event FK (model supports null=True)
                        GuestRecord.objects.create(
                            guest=guest,
                            event=None,
                            date=event_date,
                            amount=Decimal(str(row['amount'])),
                            select=row['select'],
                            event_type=row['event_type'],
                            bride_groom=row.get('bride_groom') or None,
                            pay_later=str(row['pay_later']).lower() == 'true'
                        )
                        record_new += 1
                    else:
                        # Normal event handling
                        event, _ = Event.objects.get_or_create(
                            name=row['event_name'],
                            date=event_date,
                            user=user,
                            defaults={
                                'event_type': row['event_type'],
                                'select_type': row['select'],
                                'bride_groom_name': row.get('bride_groom', '') if row['event_type'] == 'marriage' else ''
                            }
                        )
                        GuestRecord.objects.create(
                            guest=guest,
                            event=event,
                            date=event_date,
                            amount=Decimal(str(row['amount'])),
                            select=row['select'],
                            event_type=row['event_type'],
                            bride_groom=row.get('bride_groom') or None,
                            pay_later=str(row['pay_later']).lower() == 'true'
                        )
                        record_new += 1

                except Exception as e:
                    errors.append(f"Row {index}: {str(e)}")

        return Response({
            'success': True,
            'guests_created': guest_new,
            'records_created': record_new,
            'errors': errors
        }, status=status.HTTP_201_CREATED)