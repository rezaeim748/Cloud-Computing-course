import os, requests

MAILGUN_DOMAIN = os.getenv("MAILGUN_DOMAIN")
MAILGUN_API_KEY = os.getenv("MAILGUN_API_KEY")
MAILGUN_FROM = os.getenv("MAILGUN_FROM", f"noreply@{MAILGUN_DOMAIN}")

def send_email(to_email: str, subject: str, text: str):
    if not (MAILGUN_DOMAIN and MAILGUN_API_KEY):
        print("Mailgun not configured; skipping email to", to_email)
        return
    url = f"https://api.mailgun.net/v3/{MAILGUN_DOMAIN}/messages"
    data = {"from": MAILGUN_FROM, "to": [to_email], "subject": subject, "text": text}
    resp = requests.post(url, auth=("api", MAILGUN_API_KEY), data=data, timeout=30, verify=False)
    resp.raise_for_status()
