# your_app/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import CustomUser
from .tasks import delete_unverified_user

@receiver(post_save, sender=CustomUser)
def schedule_user_deletion(sender, instance, created, **kwargs):
    if created:  # Only run for newly created users
        # Schedule the task to run after 1 minute (60 seconds)
        delete_unverified_user.apply_async((instance.id,), countdown=60)