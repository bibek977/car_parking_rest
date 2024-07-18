from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .tasks import send_email_task

User=get_user_model()

@receiver(post_save,sender=User)
def send_email_signal(sender,instance,created,**kwargs):
    if created:
        send_email_task.delay(instance.email)