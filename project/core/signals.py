from django.conf import settings
from django.contrib.auth.models import User
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


@receiver(pre_save, sender=settings.AUTH_USER_MODEL)
def disable_password(sender, instance=None, created=False, **kwargs):
    if instance and not instance.pk and not instance.is_superuser:
        instance.set_unusable_password()