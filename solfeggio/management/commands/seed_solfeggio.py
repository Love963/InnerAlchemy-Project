from django.core.management.base import BaseCommand
from solfeggio.models import SolfeggioFrequency

DATA = [
    {'frequency_hz': 396, 'name': 'Liberating Guilt & Fear', 'description': 'Root chakra healing'},
    {'frequency_hz': 417, 'name': 'Undoing Situations & Facilitating Change', 'description': 'Sacral chakra'},
    {'frequency_hz': 528, 'name': 'Transformation & Miracles', 'description': 'Solar Plexus chakra'},
    {'frequency_hz': 639, 'name': 'Connecting/Relationships', 'description': 'Heart chakra'},
    {'frequency_hz': 741, 'name': 'Awakening Intuition', 'description': 'Throat chakra'},
    {'frequency_hz': 852, 'name': 'Return to Spiritual Order', 'description': 'Third Eye chakra'},
    {'frequency_hz': 963, 'name': 'Awakening Perfect State', 'description': 'Crown chakra'},
]

class Command(BaseCommand):
    help = 'Seed common Solfeggio frequencies'

    def handle(self, *args, **options):
        for row in DATA:
            SolfeggioFrequency.objects.update_or_create(
                frequency_hz=row['frequency_hz'], defaults=row
            )
        self.stdout.write(self.style.SUCCESS('Seeded Solfeggio frequencies successfully.'))
