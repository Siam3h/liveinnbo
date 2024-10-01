import requests
from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from .models import Transaction
from events.models import Event
from decouple import config
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
import os
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.shortcuts import render, redirect, get_object_or_404
from .models import Transaction
import requests


def process_payment(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    if request.method == "POST":
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        amount = event.price * 100
        transaction = Transaction.objects.create(
            email=email, phone=phone, amount=event.price, event=event
        )

        headers = {
            "Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}",
            "Content-Type": "application/json"
        }
        data = {
            "email": email,
            "amount": int(amount),
            "reference": transaction.ref,
            "callback_url": "https://web-production-0846.up.railway.app/payments/verify_payment"
        }

        url = "https://api.paystack.co/transaction/initialize"
        response = requests.post(url, json=data, headers=headers)
        response_data = response.json()

        if response_data['status']:
            transaction.ref = response_data['data']['reference']
            transaction.save()
            return redirect(response_data['data']['authorization_url'])

    return render(request, 'payments/payment.html', {'event': event})


def verify_payment(request):
    ref = request.GET.get('reference')
    transaction = get_object_or_404(Transaction, ref=ref)

    headers = {
        "Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}",
        "Content-Type": "application/json"
    }
    url = f"https://api.paystack.co/transaction/verify/{ref}"
    response = requests.get(url, headers=headers)
    response_data = response.json()

    if response_data['status'] and response_data['data']['status'] == "success":
        transaction.verified = True
        transaction.save()

        event = transaction.event
        email = transaction.email

        subject = f"Your Event Ticket: {event.title}"
        message = render_to_string('payments/events_email.html', {
            'event': event,
            'transaction': transaction,
        })

        email_message = EmailMessage(subject, message, settings.DEFAULT_FROM_EMAIL, [email])
        email_message.content_subtype = 'html'
        receipt_path = event.receipt.path
        email_message.attach_file(receipt_path)

        email_message.send()

        return redirect('thankyou', transaction_id=transaction.id)

    return render(request, 'payments/payment_failed.html')

def thankyou(request, transaction_id):
    transaction = get_object_or_404(Transaction, id=transaction_id, verified=True)
    event = transaction.event
    return render(request, 'payments/thankyou.html', {'event': event})
