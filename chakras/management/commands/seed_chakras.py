from django.core.management.base import BaseCommand
from chakras.models import Chakra

DATA = [
    dict(code='root', name='Root', sanskrit_name='Muladhara', color='Red', element='Earth'),
    dict(code='sacral', name='Sacral', sanskrit_name='Svadhisthana', color='Orange', element='Water'),
    dict(code='solar_plexus', name='Solar Plexus',sanskrit_name='Manipura', color='Yellow', element='Fire' ),
    dict(code='heart', name='Heart', sanskrit_name='Anahata', color='Green', element='Air'),
    dict(code='throat', name='Throat', sanskrit_name='Vishuddha', color='Blue', element='Ether'),
    dict(code='thrid_eye', name='Third Eye', sanskrit_name='Ajna', color='Indigo', element='Light'),
    dict(code='crown', name='Crown', sanskrit_name='Sahasrara', color='Violet', element='Thought or Cosmic Energy')

]
class Command(BaseCommand):
    help = 'Seed the 7 chakras'

    def handle(self, *args, **options):
        created = 0
        for row in DATA:
            obj, was_created = Chakra.objects.update_or_create(
                code=row['code'],
                defaults=row
            )
            created +=1 if was_created else 0
        self.stdout.write(self.style.SUCCESS(f'seeded/updated {len(DATA)} chakras (created {created}.)'))