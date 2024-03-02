from django.core.management.base import BaseCommand
from django_seed import Seed
from django.utils import timezone
from sensors_api.models import User, SensorData


class Command(BaseCommand):

    def handle(self, *args, **options):
        seeder = Seed.seeder()

        # Leverage auto_now_add for date fields, if defined
        seeder.add_entity(SensorData, 100, {'timestamp': timezone.now(), 'user': User.objects.get(id=2)})
        # Explicitly set other fields for other models
        seeder.execute()
