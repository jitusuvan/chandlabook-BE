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
    Supported:
    YYYY-MM-DD
    DD-MM-YYYY
    DD-MM-YY
    Excel date/datetime
    """

    if pd.isna(value):
        raise ValueError("Date is empty")

    if hasattr(value, "date"):
        return value.date()

    value = str(value).strip()

    for fmt in ("%Y-%m-%d", "%d-%m-%Y", "%d-%m-%y"):
        try:
            return datetime.strptime(value, fmt).date()
        except ValueError:
            pass

    raise ValueError(
        f"Invalid date '{value}'. Use YYYY-MM-DD or DD-MM-YYYY"
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

        # Read Excel
        try:
            df = pd.read_excel(file_obj, engine="openpyxl")
        except Exception as e:
            return Response(
                {"error": f"Unable to read XLSX file: {str(e)}"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Header cleanup
        df.columns = df.columns.str.strip().str.lower()

        # Old template support
        df.rename(columns={
            "event_id_or_name": "event_name",
            "guest_mobile_no": "mobile_no",
        }, inplace=True)

        required_fields = [
            "first_name",
            "last_name",
            "surname",
            "mobile_no",
            "city",
            "event_name",
            "date",
            "amount",
            "select",
            "event_type",
            "bride_groom",
            "pay_later",
        ]

        missing = [field for field in required_fields if field not in df.columns]

        if missing:
            return Response(
                {
                    "error": "Invalid header",
                    "missing": missing,
                    "received": df.columns.tolist()
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        rows = df.fillna("").to_dict(orient="records")

        guest_new = 0
        record_new = 0
        errors = []

        with transaction.atomic():
            for index, row in enumerate(rows, start=2):
                try:
                    mobile_no = str(row["mobile_no"]).strip()

                    # SAME MOBILE = SAME GUEST
                    guest, created = Guest.objects.get_or_create(
                        mobile_no=mobile_no,
                        defaults={
                            "user": user,
                            "first_name": str(row["first_name"]).strip(),
                            "last_name": str(row["last_name"]).strip(),
                            "surname": str(row["surname"]).strip(),
                            "city": str(row["city"]).strip(),
                        }
                    )

                    # If guest existed without user
                    if guest.user_id is None:
                        guest.user = user
                        guest.save()

                    if created:
                        guest_new += 1

                    event_date = parse_flexible_date(row["date"])

                    select_value = str(row["select"]).strip().lower()
                    event_type = str(row["event_type"]).strip().lower()
                    bride_groom = str(row["bride_groom"]).strip() or None
                    amount = Decimal(str(row["amount"]))
                    pay_later = (
                        str(row["pay_later"]).strip().lower() == "true"
                    )

                    # MUKEL => no event required
                    if select_value == "mukel":
                        GuestRecord.objects.create(
                            guest=guest,
                            event=None,
                            date=event_date,
                            amount=amount,
                            select=select_value,
                            event_type=event_type,
                            bride_groom=bride_groom,
                            pay_later=pay_later,
                        )
                        record_new += 1

                    else:
                        event_name = str(row["event_name"]).strip()

                        event, _ = Event.objects.get_or_create(
                            name=event_name,
                            date=event_date,
                            user=user,
                            defaults={
                                "event_type": event_type,
                                "select_type": select_value,
                                "bride_groom_name": (
                                    bride_groom
                                    if event_type == "marriage"
                                    else ""
                                ),
                            }
                        )

                        GuestRecord.objects.create(
                            guest=guest,
                            event=event,
                            date=event_date,
                            amount=amount,
                            select=select_value,
                            event_type=event_type,
                            bride_groom=bride_groom,
                            pay_later=pay_later,
                        )
                        record_new += 1

                except Exception as e:
                    errors.append(f"Row {index}: {str(e)}")

        if errors:
            return Response(
                {
                    "success": False,
                    "guests_created": guest_new,
                    "records_created": record_new,
                    "errors": errors
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response(
            {
                "success": True,
                "guests_created": guest_new,
                "records_created": record_new,
                "errors": []
            },
            status=status.HTTP_201_CREATED
        )