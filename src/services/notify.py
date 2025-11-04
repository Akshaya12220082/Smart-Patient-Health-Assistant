from __future__ import annotations

import os
import smtplib
from email.mime.text import MIMEText
from typing import Any, Dict

try:
    from twilio.rest import Client as TwilioClient
except Exception:  # Twilio may not be installed; handle gracefully
    TwilioClient = None  # type: ignore

from src.utils import load_config


def _env_or_value(value: str | None) -> str | None:
    if not value:
        return None
    if value.startswith("${") and value.endswith("}"):
        return os.environ.get(value[2:-1])
    return value


def _send_sms_twilio(to_number: str, message: str, config_path: str | None = None) -> bool:
    cfg = load_config(config_path)
    tw = cfg["services"]["twilio"]
    account_sid = _env_or_value(tw.get("account_sid"))
    auth_token = _env_or_value(tw.get("auth_token"))
    from_number = tw.get("from_number")
    if not (TwilioClient and account_sid and auth_token and from_number):
        return False
    client = TwilioClient(account_sid, auth_token)
    client.messages.create(from_=from_number, to=to_number, body=message)
    return True


def _send_email_smtp(to_email: str, subject: str, body: str, config_path: str | None = None) -> bool:
    cfg = load_config(config_path)
    smtp_cfg = cfg["services"]["smtp"]
    host = smtp_cfg.get("host")
    port = int(smtp_cfg.get("port", 587))
    username = _env_or_value(smtp_cfg.get("username"))
    password = _env_or_value(smtp_cfg.get("password"))
    from_email = smtp_cfg.get("from_email")
    if not (host and port and username and password and from_email):
        return False
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = from_email
    msg["To"] = to_email
    with smtplib.SMTP(host, port) as server:
        server.starttls()
        server.login(username, password)
        server.sendmail(from_email, [to_email], msg.as_string())
    return True


def send_sos(summary: str, config_path: str | None = None) -> Dict[str, Any]:
    cfg = load_config(config_path)
    contacts = cfg["services"].get("emergency_contacts", [])
    results = []
    for c in contacts:
        sms_ok = False
        email_ok = False
        if c.get("phone"):
            sms_ok = _send_sms_twilio(c["phone"], summary, config_path=config_path)
        if c.get("email"):
            email_ok = _send_email_smtp(c["email"], "Emergency Alert", summary, config_path=config_path)
        results.append({"contact": c, "sms": sms_ok, "email": email_ok})
    return {"sent": results}


