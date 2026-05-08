from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

import pandas as pd
from decimal import Decimal
from datetime import datetime
from django.db import transaction

from api.Guest.model import Guest
from api.GuestRecord.model import GuestRecord
from api.Event.model import Event


def parse_flexible_date(value):
    """
    Support:
    YYYY-MM-DD
    DD-MM-YYYY
    DD-MM-YY
    Excel datetime/date
    """
    if pd.isna(value):
        raise ValueError("Date is empty")

    if hasattr(value, "date"):
        return value.date()

    value = str(value).strip()

    for fmt in ['%Y-%m-%d', '%d-%m-%Y', '%d-%m-%y']:
        try:
            return datetime.strptime(value, fmt).date()
        except ValueError:
            continue

    raise ValueError(
        f"Invalid date '{value}'. Expected: YYYY-MM-DD, DD-MM-YYYY, or DD-MM-YY"
    )


class BulkGuestImportWithRecordsView(APIView):
    parser_classes = [MultiPartParser, FormParser]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        file_obj = request.FILES.get("file")

        if not file_obj:
            return Response(
                {"error": "XLSX file required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        user = request.user

        try:
            filename = file_obj.name
            if filename.endswith(".xls"):
                df = pd.read_excel(file_obj, engine="xlrd")
            else:
                df = pd.read_excel(file_obj, engine="openpyxl")
        except Exception as e:
            return Response(
                {"error": f"Unable to read XLSX file: {str(e)}"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # header cleanup
        df.columns = df.columns.str.strip().str.lower()
        
        df.rename(columns={
           "event_id_or_name": "event_name",
           "guest_mobile_no": "mobile_no",
           }, inplace=True)
        
        
        required_fields = [
           'first_name','last_name','surname','mobile_no','city',
           'event_name','date','amount','select',
           'event_type','bride_groom','pay_later'
             ]

        if not all(field in df.columns for field in required_fields):
            return Response(
                {
                    "error": f"Invalid header. Required: {required_fields}. Supports XLSX"
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        rows = df.fillna("").to_dict(orient="records")

        guest_new = 0
        record_new = 0
        errors = []

        with transaction.atomic():
            for index, row in enumerate(rows, start=2):  # Excel row starts after header
                try:
                    guest, created = Guest.objects.filter(user=user).get_or_create(
                        mobile_no=str(row['mobile_no']).strip(),
                        defaults={
                            'user': user,
                            'first_name': str(row['first_name']).strip(),
                            'last_name': str(row['last_name']).strip(),
                            'surname': str(row['surname']).strip(),
                            'city': str(row['city']).strip(),
                        }
                    )

                    if created:
                        guest_new += 1

                    event_date = parse_flexible_date(row['date'])

                    if str(row['select']).strip().lower() == "mukel":
                        _, created_record = GuestRecord.objects.get_or_create(
                            guest=guest,
                            date=event_date,
                            amount=Decimal(str(row['amount'])),
                            select=str(row['select']).strip(),
                            defaults={
                                'event': None,
                                'event_type': str(row['event_type']).strip(),
                                'bride_groom': str(row['bride_groom']).strip() or None,
                                'pay_later': str(row['pay_later']).strip().lower() == "true"
                            }
                        )
                        if created_record:
                            record_new += 1

                    else:
                        event, _ = Event.objects.get_or_create(
                            name=str(row['event_name']).strip(),
                            date=event_date,
                            user=user,
                            defaults={
                                'event_type': str(row['event_type']).strip(),
                                'select_type': str(row['select']).strip(),
                                'bride_groom_name': (
                                    str(row['bride_groom']).strip()
                                    if str(row['event_type']).strip().lower() == "marriage"
                                    else ""
                                )
                            }
                        )

                        _, created_record = GuestRecord.objects.get_or_create(
                            guest=guest,
                            event=event,
                            date=event_date,
                            amount=Decimal(str(row['amount'])),
                            select=str(row['select']).strip(),
                            defaults={
                                'event_type': str(row['event_type']).strip(),
                                'bride_groom': str(row['bride_groom']).strip() or None,
                                'pay_later': str(row['pay_later']).strip().lower() == "true"
                            }
                        )
                        if created_record:
                            record_new += 1

                except Exception as e:
                    errors.append(f"Row {index}: {str(e)}")

        return Response(
            {
                "success": True,
                "guests_created": guest_new,
                "records_created": record_new,
                "errors": errors
            },
            status=status.HTTP_201_CREATED
        )
