from django.test import TestCase

# Create your tests here.
# core/tests.py
from django.test import TestCase
from django.contrib.auth import get_user_model
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
        # Create a test user
        self.user = User.objects.create_user(
            email="testuser@example.com", username="testuser", password="strongpass123"
        )

        # Solfeggio Frequency
        self.freq = SolfeggioFrequency.objects.create(frequency_hz=528, name="Love Frequency")

        # Chakras master
        self.root_chakra = Chakra.objects.create(code='root', name='Root', sanskrit_name='Muladhara')

    # -----------------------------
    # Solfeggio Frequency Tests
    # -----------------------------
    def test_solfeggio_creation(self):
        freq = SolfeggioFrequency.objects.get(frequency_hz=528)
        self.assertEqual(freq.name, "Love Frequency")

    # -----------------------------
    # Meditation Session Tests
    # -----------------------------
    # -----------------------------
    # Meditation Session Tests
    # -----------------------------
    def test_meditation_with_frequency_and_spirit_level(self):
        med = MeditationSession.objects.create(
            user=self.user,
            title="Morning Clarity",
            description="Focus meditation",
            duration_minutes=20,
            clarity_score=9,
            mood_before="Calm",
            mood_after="Grateful",
            spirit_level="Balanced",   # ✅ new field
            solfeggio_frequency=self.freq
        )

        # Assertions
        self.assertEqual(med.solfeggio_frequency.name, "Love Frequency")
        self.assertEqual(med.user.username, "testuser")
        self.assertEqual(med.spirit_level, "Balanced")
        self.assertEqual(med.mood_after, "Grateful")
        self.assertEqual(str(med), f"{med.title} - {self.user.username}")


    # -----------------------------
    # Chakra Logs Tests
    # -----------------------------
    def test_chakra_log_creation(self):
        log = ChakraLog.objects.create(
            user=self.user,
            chakra=self.root_chakra,
            state='balanced',
            intensity=7,
            solfeggio_frequency=self.freq
        )
        self.assertEqual(log.chakra.name, 'Root')
        self.assertEqual(log.solfeggio_frequency.frequency_hz, 528)

    # -----------------------------
    # Sexual Energy Tests
    # -----------------------------
    def test_sexual_energy_session(self):
        ses = SexualEnergySession.objects.create(
            user=self.user,
            intention='creativity',
            duration_minutes=15
        )
        self.assertEqual(ses.intention, 'creativity')

        sel = SexualEnergyLog.objects.create(
            user=self.user,
            urges_felt=True,
            energy_level=8,
            redirect_activity='Meditation'
        )
        self.assertEqual(sel.energy_level, 8)

    # -----------------------------
    # Gratitude & Visualization Tests
    # -----------------------------
    def test_gratitude_and_visualization(self):
        gratitude = GratitudeEntry.objects.create(
            user=self.user,
            content="Grateful for health",
            gratitude_score=9,
            solfeggio_frequency=self.freq
        )
        self.assertEqual(gratitude.gratitude_score, 9)

        viz = VisualizationAffirmation.objects.create(
            user=self.user,
            title="Abundance Visualization",
            content="I am abundant",
            solfeggio_frequency=self.freq
        )
        self.assertEqual(viz.solfeggio_frequency.frequency_hz, 528)

    # -----------------------------
    # Cold Shower & Workout Tests
    # -----------------------------
    def test_cold_shower_and_workout(self):
        cs = ColdShowerLog.objects.create(
            user=self.user,
            mood_before='tired',
            mood_after='refreshed',
            resistance_level=7
        )
        self.assertEqual(cs.resistance_level, 7)

        workout = WorkoutSession.objects.create(
            user=self.user,
            type='yoga',
            duration_minutes=30,
            energy_effect=8
        )
        self.assertEqual(workout.type, 'yoga')

    # -----------------------------
    # Soul Notes & Nutrition
    # -----------------------------
    def test_soulnote_and_nutrition(self):
        note = SoulNote.objects.create(
            user=self.user,
            title="Morning Insight",
            content="Felt very creative today"
        )
        self.assertEqual(note.user.username, 'testuser')

        nutrition = NutritionLog.objects.create(
            user=self.user,
            meal_type='breakfast',
            food_items="Oats and banana",
            calories=300,
            hydration_liters=0.5,
            energy_effect=7,
            mood_effect=8
        )
        self.assertEqual(nutrition.meal_type, 'breakfast')

    # -----------------------------
    # Sleep Logs & Stages
    # -----------------------------
    def test_sleep_logs_and_stages(self):
        sleep = SleepLog.objects.create(
            user=self.user,
            sleep_start="2025-08-23 22:00",
            sleep_end="2025-08-24 06:00",
            mood_after="rested"
        )
        self.assertEqual(sleep.total_duration.total_seconds(), 8*3600)

        stage_type = SleepStageType.objects.create(name="REM")
        stage = SleepStage.objects.create(
            sleep_log=sleep,
            stage_type=stage_type,
            duration_minutes=90
        )
        self.assertEqual(stage.duration_minutes, 90)

        rec = SleepSolfeggioRecommendation.objects.create(
            sleep_log=sleep,
            frequency="528Hz",
            reason="Healing"
        )
        self.assertEqual(rec.frequency, "528Hz")
