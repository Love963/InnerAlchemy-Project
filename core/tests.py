from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta

from solfeggio.models import SolfeggioFrequency
from meditation.models import MeditationSession
from chakras.models import Chakra, ChakraLog
from sexualenergy.models import SexualEnergySession, SexualEnergyLog
from gratitude.models import GratitudeEntry
from visualizations.models import VisualizationAffirmation
from coldshowers.models import ColdShowerLog
from workouts.models import WorkoutSession
from soulnotes.models import SoulNote
from nutrition.models import NutritionLog
from sleep.models import SleepLog, SleepStageType, SleepStage, SleepSolfeggioRecommendation

User = get_user_model()


class InnerAlchemyTests(TestCase):

    def setUp(self):
        # Test user
        self.user = User.objects.create_user(
            email="testuser@example.com", username="testuser", password="strongpass123"
        )
        # Core frequency
        self.freq = SolfeggioFrequency.objects.create(
            frequency_hz=528, name="Love Frequency"
        )
        # Chakra master
        self.root_chakra = Chakra.objects.create(
            code="root", name="Root", sanskrit_name="Muladhara"
        )


    # Solfeggio
    def test_solfeggio_creation(self):
        freq = SolfeggioFrequency.objects.get(frequency_hz=528)
        self.assertEqual(freq.name, "Love Frequency")

    # Meditation
    def test_meditation_session(self):
        med = MeditationSession.objects.create(
            user=self.user,
            title="Morning Clarity",
            description="Focus meditation",
            duration_minutes=20,
            clarity_score=9,
            mood_before="Calm",
            mood_after="Grateful",
            solfeggio_frequency=self.freq,
        )
        self.assertEqual(med.user.username, "testuser")
        self.assertEqual(med.solfeggio_frequency.name, "Love Frequency")
        self.assertEqual(med.mood_after, "Grateful")

    # Chakra Logs
    def test_chakra_log_creation(self):
        log = ChakraLog.objects.create(
            user=self.user,
            chakra=self.root_chakra,
            state="balanced",
            intensity=7,
            solfeggio_frequency=self.freq,
        )
        self.assertEqual(log.chakra.name, "Root")
        self.assertEqual(log.solfeggio_frequency.frequency_hz, 528)

    # Sexual Energy
    def test_sexual_energy_session_and_log(self):
        ses = SexualEnergySession.objects.create(
            user=self.user, intention="creativity", duration_minutes=15
        )
        self.assertEqual(ses.intention, "creativity")

        sel = SexualEnergyLog.objects.create(
            user=self.user,
            urges_felt=True,
            energy_level=8,
            redirect_activity="Meditation",
        )
        self.assertEqual(sel.energy_level, 8)

    # Gratitude & Visualization
    def test_gratitude_and_visualization(self):
        gratitude = GratitudeEntry.objects.create(
            user=self.user,
            content="Grateful for health",
            gratitude_score=9,
            solfeggio_frequency=self.freq,
        )
        self.assertEqual(gratitude.gratitude_score, 9)

        viz = VisualizationAffirmation.objects.create(
            user=self.user,
            title="Abundance Visualization",
            content="I am abundant",
            solfeggio_frequency=self.freq,
        )
        self.assertEqual(viz.solfeggio_frequency.frequency_hz, 528)

    # Cold Shower & Workout
    def test_cold_shower_and_workout(self):
        cs = ColdShowerLog.objects.create(
            user=self.user,
            mood_before="tired",
            mood_after="refreshed",
            resistance_level=7,
        )
        self.assertEqual(cs.resistance_level, 7)

        workout = WorkoutSession.objects.create(
            user=self.user, type="yoga", duration_minutes=30, energy_effect=8
        )
        self.assertEqual(workout.type, "yoga")

    # Soul Notes & Nutrition
    def test_soulnote_and_nutrition(self):
        note = SoulNote.objects.create(
            user=self.user, title="Morning Insight", content="Felt very creative today"
        )
        self.assertEqual(note.user.username, "testuser")

        nutrition = NutritionLog.objects.create(
            user=self.user,
            meal_type="breakfast",
            food_items="Oats and banana",
            calories=300,
            hydration_liters=0.5,
            energy_effect=7,
            mood_effect=8,
        )
        self.assertEqual(nutrition.meal_type, "breakfast")
        self.assertAlmostEqual(nutrition.nutrition_score, 7.5)

    # Sleep Logs & Stages
    def test_sleep_logs_and_stages(self):
        start = timezone.now().replace(hour=22, minute=0, second=0, microsecond=0)
        end = start + timedelta(hours=8)

        sleep = SleepLog.objects.create(
            user=self.user, sleep_start=start, sleep_end=end, mood_after="rested"
        )
        self.assertEqual(sleep.total_duration.total_seconds(), 8 * 3600)

        stage_type = SleepStageType.objects.create(name="REM")
        stage = SleepStage.objects.create(
            sleep_log=sleep, stage_type=stage_type, duration_minutes=90
        )
        self.assertEqual(stage.duration_minutes, 90)

        rec = SleepSolfeggioRecommendation.objects.create(
            sleep_log=sleep, frequency="528Hz", reason="Healing"
        )
        self.assertEqual(rec.frequency, "528Hz")
