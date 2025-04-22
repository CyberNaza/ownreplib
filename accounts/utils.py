
from django.core.mail import send_mail

def send_verification_email(email, code):
    subject = "Your Verification Code"
    message = f"Hello,\n\nYour verification code is: {code}\n\nThank you for registering!"
    from_email = None  # Uses DEFAULT_FROM_EMAIL from settings
    recipient_list = [email]

    send_mail(subject, message, from_email, recipient_list)
