from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from accounts.models import TempData, User


@receiver(post_save, sender=User)
def create_temp_data(sender, instance, created, **kwargs):
    if created:
        TempData.objects.get_or_create(user=instance)

        if instance.is_admin or instance.is_staff:
            instance.first_name = instance.username

        elif instance.email:
            instance.username = instance.email

        instance.save()


@receiver(post_delete, sender=User)
def create_temp_data(sender, instance, created, **kwargs):
    TempData.objects.filter(user=instance).delete()
