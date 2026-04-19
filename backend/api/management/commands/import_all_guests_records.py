from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
import csv
from decimal import Decimal
from datetime import datetime
from django.db import transaction

from api.Guest.model import Guest
from api.GuestRecord.model import GuestRecord
from api.Event.model import Event


class Command(BaseCommand):
    help = 'Import guests and records from CSV'

    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str)
        parser.add_argument('--user', type=str, required=True)

    def handle(self, *args, **options):
        file_path = options['file_path']
        username = options['user']

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'User {username} not found'))
            return

        with open(file_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            rows = list(reader)

        guest_new = 0
        record_new = 0
        errors = []

        with transaction.atomic():
            for index, row in enumerate(rows, start=1):
                try:
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

                    event_date = datetime.strptime(row['date'], '%Y-%m-%d').date()

                    event, _ = Event.objects.get_or_create(
                        name=row['event_name'],
                        date=event_date,
                        user=user,
                        defaults={
                            'event_type': row['event_type'],
                            'select_type': row['select'],
                            'bride_groom_name': row.get('bride_groom', '')
                        }
                    )

                    GuestRecord.objects.create(
                        guest=guest,
                        event=event,
                        date=event_date,
                        amount=Decimal(str(row['amount'])),
                        select=row['select'],
                        event_type=row['event_type'],
                        bride_groom=row.get('bride_groom'),
                        pay_later=str(row['pay_later']).lower() == 'true'
                    )

                    record_new += 1

                except Exception as e:
                    errors.append(f"Row {index}: {str(e)}")

        self.stdout.write(self.style.SUCCESS(
            f"Done → Guests: {guest_new}, Records: {record_new}, Errors: {len(errors)}"
        ))