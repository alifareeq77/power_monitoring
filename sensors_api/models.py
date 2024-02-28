from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
import uuid
from django.contrib.auth import get_user_model

# Create your models here.
User = get_user_model()



class SensorData(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    voltage = models.FloatField()
    current = models.FloatField()
    power = models.FloatField(blank=True, null=True)  # Added field for power
    timestamp = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # Calculate power before saving
        self.power = self.voltage * self.current
        super().save(*args, **kwargs)


class UserDashboard(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    dashboard_link = models.CharField(max_length=100, unique=True)


@receiver(post_save, sender=User)
def create_user_dashboard(sender, instance, created, **kwargs):
    if created:
        # Generate unique dashboard link
        dashboard_link = str(uuid.uuid4())[:8]  # Generate a random 8-character string
        UserDashboard.objects.create(user=instance, dashboard_link=dashboard_link)


