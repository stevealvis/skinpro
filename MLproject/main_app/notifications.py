import os
from typing import List

import requests
from django.conf import settings
from django.core.mail import send_mail


def _get_notification_channels() -> List[str]:
    raw = os.getenv(
        "APPOINTMENT_NOTIFICATION_CHANNELS",
        getattr(settings, "APPOINTMENT_NOTIFICATION_CHANNELS", "email"),
    )
    return [c.strip() for c in str(raw).split(",") if c.strip()]


def _send_email(to_email: str, subject: str, body: str) -> None:
    if not to_email:
        return

    from_email = getattr(settings, "DEFAULT_FROM_EMAIL", None)
    try:
        send_mail(subject, body, from_email, [to_email], fail_silently=True)
    except Exception:
        return


def _send_twilio_message(to_number: str, body: str, channel: str) -> None:
    account_sid = getattr(settings, "TWILIO_ACCOUNT_SID", "")
    auth_token = getattr(settings, "TWILIO_AUTH_TOKEN", "")

    if not account_sid or not auth_token:
        return

    if channel == "sms":
        from_number = getattr(settings, "TWILIO_FROM_SMS", "")
        to_value = to_number
    elif channel == "whatsapp":
        from_number = getattr(settings, "TWILIO_FROM_WHATSAPP", "")
        if to_number.startswith("whatsapp:"):
            to_value = to_number
        else:
            to_value = "whatsapp:" + to_number
    else:
        return

    if not from_number or not to_value:
        return

    url = (
        "https://api.twilio.com/2010-04-01/Accounts/"
        + account_sid
        + "/Messages.json"
    )

    data = {
        "To": to_value,
        "From": from_number,
        "Body": body,
    }

    try:
        requests.post(url, data=data, auth=(account_sid, auth_token), timeout=5)
    except Exception:
        return


def send_appointment_notifications(consultation_obj) -> None:
    if consultation_obj is None:
        return

    patient_obj = consultation_obj.patient
    doctor_obj = consultation_obj.doctor

    if patient_obj is None or doctor_obj is None:
        return

    user = patient_obj.user
    email = user.email
    phone = patient_obj.mobile_no

    subject = "Your medical consultation is scheduled"
    body_parts = [
        "Dear " + patient_obj.name + ",",
        "",
        "Your consultation has been scheduled.",
        "Doctor: Dr. " + doctor_obj.name,
        "Specialization: " + doctor_obj.specialization,
        "Status: " + consultation_obj.status,
    ]

    if consultation_obj.consultation_date:
        body_parts.append(
            "Date: " + consultation_obj.consultation_date.strftime("%Y-%m-%d")
        )

    body_parts.append("")
    body_parts.append(
        "You can also open the website to join the online consultation."
    )

    body_text = "\n".join(body_parts)

    channels = _get_notification_channels()

    if "email" in channels and email:
        _send_email(email, subject, body_text)

    if phone:
        if "sms" in channels:
            _send_twilio_message(phone, body_text, "sms")
        if "whatsapp" in channels:
            _send_twilio_message(phone, body_text, "whatsapp")

