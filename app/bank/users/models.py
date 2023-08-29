from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User

# Create your models here.


class AuthUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    reg_date = models.DateTimeField(auto_created=True, auto_now_add=True)
    active = models.BooleanField(default=True)

    def __str__(self) -> str:
        return f"{self.user.email} - {self.active}"

    class Meta:
        ordering = ["-reg_date"]


@receiver(post_save, sender=AuthUser)
def notify_account_create(sender, instance, created, **kwargs):
    if created:
        pass  # TODO: enable logging for successfull account creation
