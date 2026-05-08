from io import BytesIO

import pandas as pd

from django.http import HttpResponse
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from api.Guest.model import Guest
from api.GuestRecord.model import GuestRecord


class ExportGuestRecordsXlsxView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        # Fetch user-scoped data
        guests_qs = Guest.objects.filter(user=user).only(
            "first_name",
            "last_name",
            "surname",
            "mobile_no",
            "city",
        )

        records_qs = (
            GuestRecord.objects.filter(guest__user=user)
            .select_related("guest", "event")
            .only(
                "date",
                "amount",
                "select",
                "event_type",
                "bride_groom",
                "pay_later",
                "guest__first_name",
                "guest__last_name",
                "guest__surname",
                "guest__mobile_no",
                "guest__city",
                "event__name",
            )
            .order_by("-date")
        )

        # One-sheet format MUST match bulk import headers
        # See: api/Guest/bulk_import_view.py -> required_fields
        rows = []
        for rec in records_qs:
            guest = rec.guest
            rows.append(
                {
                    "first_name": guest.first_name or "",
                    "last_name": guest.last_name or "",
                    "surname": guest.surname or "",
                    "mobile_no": guest.mobile_no or "",
                    "city": guest.city or "",
                    "event_name": rec.event.name if rec.event_id else "",
                    "date": rec.date,
                    "amount": rec.amount,
                    "select": rec.select or "",
                    "event_type": rec.event_type or "",
                    "bride_groom": rec.bride_groom or "",
                    "pay_later": "true" if rec.pay_later else "false",
                }
            )

        # Also include guests that have no records? Import requires record fields,
        # so we keep it record-based export (matches bulk import use-case).
        df = pd.DataFrame(
            rows,
            columns=[
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
            ],
        )

        buffer = BytesIO()
        with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
            df.to_excel(writer, index=False, sheet_name="Sheet1")

        buffer.seek(0)

        filename = "guest_records_export.xlsx"
        response = HttpResponse(
            buffer,
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )
        response["Content-Disposition"] = f"attachment; filename={filename}"
        return response

