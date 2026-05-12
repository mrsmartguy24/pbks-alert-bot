import time
import requests

URLS = [
    "https://www.district.in/events/punjab-kings-team"
]

BOT_TOKEN = "8038967641:AAHG8cZNFTRBDwjYDZVp-GNj1ECSRdEh250"
CHAT_ID = "823023213"

 CHECK_INTERVAL = 10

last_html = ""


def send_telegram(message):
    telegram_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    payload = {
        "chat_id": CHAT_ID,
        "text": message
    }

    requests.post(telegram_url, data=payload)


def check_sale():
    global last_html

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    positive_keywords = [
        "book now",
        "buy now",
        "sale is live",
        "grab tickets",
        "book tickets",
        "tickets available"
    ]

    negative_keywords = [
        "coming soon",
        "sold out"
    ]

    for url in URLS:

        response = requests.get(url, headers=headers, timeout=15)

        html = response.text.lower()

        positive = any(word in html for word in positive_keywords)

        negative = any(word in html for word in negative_keywords)

        # Trigger if page changes significantly
        if last_html != "" and html != last_html:

            if positive and not negative:
                return True

        last_html = html

    return False


print("Monitoring PBKS ticket page...")

while True:

    try:

        live = check_sale()

        print("Checked...")

        if live:

            print("SALE LIVE!")

            send_telegram(
                "PBKS tickets are LIVE!\n\nhttps://www.district.in/events/punjab-kings-team"
            )

            break

        time.sleep(CHECK_INTERVAL)

    except Exception as e:

        print("Error:", e)

        time.sleep(CHECK_INTERVAL)
