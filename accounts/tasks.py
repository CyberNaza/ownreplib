# your_app/tasks.py
from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from .models import CustomUser

@shared_task
def delete_unverified_user(user_id):
    try:
        user = CustomUser.objects.get(id=user_id)
        if not user.is_verified:
            user.delete()
            print(f"Deleted unverified user: {user.email}")
        else:
            print(f"User {user.email} is verified, not deleted.")
    except CustomUser.DoesNotExist:
        print(f"User with ID {user_id} does not exist.")