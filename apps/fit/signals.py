from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from ..fitprofile.models import FitProfile

@receiver(post_save,sender=User)
def crear_profile_usuerio(sender,instance,created,**kwargs):
    if created:
        FitProfile.objects.create(user=instance)
