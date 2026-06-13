import requests
import smtplib
import os
from datetime import date
from email.mime.text import MIMEText

api_key = os.environ.get("WEATHER_API_KEY")


def get_weather(city="Thiruvananthapuram"):
    url = f"https://wttr.in/{city}?format=3"

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.text.strip()

    except Exception as e:
        return f"Weather unavailable ({e})"


def get_quote():
    url = "https://zenquotes.io/api/random"

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        data = response.json()
        quote = data[0]["q"]
        author = data[0]["a"]

        return f'"{quote}" - {author}'

    except Exception as e:
        return f"Quote unavailable ({e})"


def get_fact():
    url = "https://uselessfacts.jsph.pl/api/v2/facts/random"

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        data = response.json()
        return data["text"]

    except Exception as e:
        return f"Fact unavailable ({e})"


def send_email(summary_text):
    sender = os.environ.get("EMAIL_ADDRESS")
    password = os.environ.get("EMAIL_APP_PASSWORD")
    receiver = os.environ.get("RECIPIENT_EMAIL")

    msg = MIMEText(summary_text)

    msg["Subject"] = "Pulse Daily Summary"
    msg["From"] = sender
    msg["To"] = receiver

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(sender, password)
        server.send_message(msg)


def build_summary():
    today = date.today().strftime("%A, %d %B %Y")

    weather = get_weather()
    quote = get_quote()
    fact = get_fact()

    summary = f"""
========================================================
PULSE - Daily Summary
{today}
========================================================

WEATHER
{weather}

QUOTE
{quote}

FACT
{fact}

========================================================
"""

    return summary


def run():
    summary = build_summary()

    print(summary)

    with open("daily_summary.txt", "w", encoding="utf-8") as f:
        f.write(summary)

    send_email(summary)

    print("Pulse ran successfully")
    print("Email sent successfully")


if __name__ == "__main__":
    run()
