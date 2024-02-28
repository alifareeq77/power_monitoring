from django.core.management.base import BaseCommand
from django_seed import Seed
from django.utils import timezone
from sensors_api.models import Voltage, Current, Power, User


class Command(BaseCommand):

    def handle(self, *args, **options):
        seeder = Seed.seeder()

        # Leverage auto_now_add for date fields, if defined
        seeder.add_entity(Voltage, 100, {'date': timezone.now(), 'user': User.objects.get(id=2)})
        seeder.add_entity(Current, 100, {'date': timezone.now(), 'user': User.objects.get(id=2)})
        seeder.add_entity(Power, 100, {'date': timezone.now(), 'user': User.objects.get(id=2)})

        # Explicitly set other fields for other models

        seeder.execute()
