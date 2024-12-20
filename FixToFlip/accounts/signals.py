from django.db.models.signals import post_save
from django.dispatch import receiver

from FixToFlip.accounts.models import BaseAccount, Profile


@receiver(post_save, sender=BaseAccount)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
