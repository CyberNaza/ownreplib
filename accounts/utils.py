from django.utils import timezone
from datetime import timedelta
from .models import CustomUser
from django.core.mail import send_mail

def send_verification_email(email, code):
    subject = "Your Verification Code"
    message = f"Hello,\n\nYour verification code is: {code}\n\nThank you for registering!"
    from_email = None  
    recipient_list = [email]

    send_mail(subject, message, from_email, recipient_list)



def delete_old_unverified_users():
    threshold = timezone.now() - timedelta(minutes=1)
    CustomUser.objects.filter(is_verified=False, date_joined__lt=threshold).delete()
