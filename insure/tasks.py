import requests

from django.template.loader import get_template

from celery import shared_task


@shared_task
def send_response_notification(response):
    body_template = get_template("insure/mail.html")
    params = {
        "format": "json",
        "api_key": "6hnncnaoxqgbnqcsejn1omx467iksgk8mfjbpd7e",
        "email": response["email"],
        "sender_name": "maxim",
        "sender_email": "insure2022@yandex.ru",
        "subject": f"Thank you for leaving a request for the produc {response['product']}",
        "body": body_template.render(response),
        "list_id": 1,
    }
    requests.post("https://api.unisender.com/ru/api/sendEmail", params=params)
    return "as"
