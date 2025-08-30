from datetime import date, timedelta
from django.utils import timezone
from django.db.models import Avg, Sum, Q, Count

# Import models from apps
from meditation.models import MeditationSession
from breathwork.models import BreathworkSession
from workouts.models import WorkoutSession
from nutrition.models import NutritionLog
from sleep.models import SleepLog
from gratitude.models import GratitudeEntry
from coldshowers.models import ColdShowerLog
from sexualenergy.models import SexualEnergyLog
from chakras.models import ChakraLog
from soulnotes.models import SoulNote
from visualizations.models import VisualizationAffirmation

def period_bounds(period: str, start_date=None):
    today = timezone.localdate()
    if period == "weekly":
        if start_date:
            start = start_date
        else:
            # last full week ending today (7 days)
            start = today - timedelta(days=6)
        end = start + timedelta(days=6)
    else:  # monthly
        if start_date:
            start = start_date
        else:
            start = today.replace(day=1)
        # naive month end: if start provided may need calendar logic; here:
        next_month = (start.replace(day=28) + timedelta(days=4)).replace(day=1)
        end = (next_month - timedelta(days=1))
    return start, end

def normalize(value, min_v=0, max_v=10):
    """
    Normalize a value from [min_v, max_v] to 0-100.
    Prevent divide-by-zero.
    """
    try:
        v = float(value)
    except (TypeError, ValueError):
        return None
    if max_v == min_v:
        return 0
    score = (v - min_v) / (max_v - min_v) * 100
    if score < 0: score = 0
    if score > 100: score = 100
    return round(score, 1)

def safe_avg(queryset, field):

    # Return average of `field` from queryset if exists else None

    agg = queryset.aggregate(avg=Avg(field))
    return agg.get("avg")

def compute_metrics_for_user(user, period="weekly", start_date=None):
    # Compute a dictionary of metric - {score, sources...} for the given user and period bounds.
    # This function is intentionally explicit so you can extend mapping easily.
    start, end = period_bounds(period, start_date)
    # convert to datetimes where models use DateTimeField vs DateField as needed
    start_dt = timezone.datetime.combine(start, timezone.datetime.min.time())
    end_dt = timezone.datetime.combine(end, timezone.datetime.max.time())

    # Meditation: clarity_score (1-10) 
    med_qs = MeditationSession.objects.filter(user=user, date__range=(start_dt, end_dt))
    med_clarity_avg = safe_avg(med_qs, "clarity_score")
    med_clarity_score = normalize(med_clarity_avg, 0, 10) if med_clarity_avg is not None else None

    # Breathwork: energy_level (1-10) 
    breath_qs = BreathworkSession.objects.filter(user=user, date__range=(start, end))
    breath_energy_avg = safe_avg(breath_qs, "energy_level")
    breath_energy_score = normalize(breath_energy_avg, 1, 10) if breath_energy_avg is not None else None

    # Workouts: energy_effect (1-10)
    workout_qs = WorkoutSession.objects.filter(user=user, date__range=(start, end))
    workout_energy_avg = safe_avg(workout_qs, "energy_effect")
    workout_energy_score = normalize(workout_energy_avg, 1, 10) if workout_energy_avg is not None else None

    # Nutrition: energy_effect & mood_effect (1-10) take average 
    nut_qs = NutritionLog.objects.filter(user=user, date__range=(start, end))
    nut_energy_avg = safe_avg(nut_qs, "energy_effect")
    nut_mood_avg = safe_avg(nut_qs, "mood_effect")
    nutrition_combined = None
    if nut_energy_avg is not None and nut_mood_avg is not None:
        nutrition_combined = (nut_energy_avg + nut_mood_avg) / 2.0
    elif nut_energy_avg is not None:
        nutrition_combined = nut_energy_avg
    elif nut_mood_avg is not None:
        nutrition_combined = nut_mood_avg
    nutrition_score = normalize(nutrition_combined, 1, 10) if nutrition_combined is not None else None

    # Sleep: quality_score (1-10)
    sleep_qs = SleepLog.objects.filter(user=user, date__range=(start, end))
    # SleepLog may have quality_score field; aggregate
    sleep_quality_avg = safe_avg(sleep_qs, "quality_score")
    sleep_score = normalize(sleep_quality_avg, 1, 10) if sleep_quality_avg is not None else None

    # Gratitude: gratitude_score (0-10)
    grat_qs = GratitudeEntry.objects.filter(user=user, date__range=(start, end))
    grat_avg = safe_avg(grat_qs, "gratitude_score")
    gratitude_score = normalize(grat_avg, 0, 10) if grat_avg is not None else None

    # Cold showers: resistance_level (1-10) -lower resistance is "better" (we invert) 
    cold_qs = ColdShowerLog.objects.filter(user=user, date__range=(start_dt, end_dt))
    cold_res_avg = safe_avg(cold_qs, "resistance_level")
    cold_score = None
    if cold_res_avg is not None:
        # invert: lower resistance -> higher score
        inverted = 11 - float(cold_res_avg)  # map 1->10, 10->1
        cold_score = normalize(inverted, 1, 10)

    # Sexual energy logs: energy_level (1-10) 
    senergy_qs = SexualEnergyLog.objects.filter(user=user, logged_at__range=(start_dt, end_dt))
    senergy_avg = safe_avg(senergy_qs, "energy_level")
    sexual_energy_score = normalize(senergy_avg, 1, 10) if senergy_avg is not None else None

    # Chakras: intensity (1-10) averaged across chakra logs 
    chakra_qs = ChakraLog.objects.filter(user=user, date__range=(start, end))
    chakra_intensity_avg = safe_avg(chakra_qs, "intensity")
    chakra_score = normalize(chakra_intensity_avg, 1, 10) if chakra_intensity_avg is not None else None

    # SoulNotes: map mood to score (we map positive moods)
    mood_map = {
        "happy": 8, "grateful": 9, "motivated": 8, "focused": 7,
        "inspired": 8, "calm": 7, "peaceful": 8, "creative": 7,
        "flow_state": 9, "energetic": 8, "spiritually_connected": 9, "neutral":5
    }
    notes_qs = SoulNote.objects.filter(user=user, date_created__date__range=(start, end))
    if notes_qs.exists():
        mapped = []
        for n in notes_qs:
            if n.mood:
                mapped.append(mood_map.get(n.mood, 5))
        soulnotes_avg = (sum(mapped) / len(mapped)) if mapped else None
        soulnotes_score = normalize(soulnotes_avg, 1, 10) if soulnotes_avg is not None else None
    else:
        soulnotes_score = None

    # VisualizationAffirmations: activity level (count)
    viz_count = VisualizationAffirmation.objects.filter(user=user, date_created__date__range=(start, end)).count()
    # Map 0..X to 0..100 with a sensible cap at 10 uses/week or 40/month.
    cap = 10 if period == "weekly" else 40
    viz_score = normalize(min(viz_count, cap), 0, cap) if viz_count is not None else None

    # Compose high-level metrics (you can add more)
    metrics = {}

    # Energy: combine breathwork, workouts, nutrition, sexual energy
    energy_sources = {}
    parts = []
    if breath_energy_score is not None:
        energy_sources["breathwork"] = breath_energy_score
        parts.append(breath_energy_score)
    if workout_energy_score is not None:
        energy_sources["workouts"] = workout_energy_score
        parts.append(workout_energy_score)
    if nutrition_score is not None:
        energy_sources["nutrition"] = nutrition_score
        parts.append(nutrition_score)
    if sexual_energy_score is not None:
        energy_sources["sexual_energy"] = sexual_energy_score
        parts.append(sexual_energy_score)
    energy_score = round(sum(parts) / len(parts), 1) if parts else None
    metrics["energy"] = {"score": energy_score, "sources": energy_sources}

    # Clarity: meditation clarity + sleep + soulnotes (mapped)
    clarity_parts = []
    clarity_sources = {}
    if med_clarity_score is not None:
        clarity_sources["meditation"] = med_clarity_score
        clarity_parts.append(med_clarity_score)
    if sleep_score is not None:
        clarity_sources["sleep"] = sleep_score
        clarity_parts.append(sleep_score)
    if soulnotes_score is not None:
        clarity_sources["soul_notes"] = soulnotes_score
        clarity_parts.append(soulnotes_score)
    clarity_score = round(sum(clarity_parts) / len(clarity_parts), 1) if clarity_parts else None
    metrics["clarity"] = {"score": clarity_score, "sources": clarity_sources}

    # Vibration / Gratitude / Spirit-level: gratitude, visualization, chakra
    vibration_parts = []
    vibration_sources = {}
    if gratitude_score is not None:
        vibration_parts.append(gratitude_score)
        vibration_sources["gratitude"] = gratitude_score
    if viz_score is not None:
        vibration_parts.append(viz_score)
        vibration_sources["visualizations"] = viz_score
    if chakra_score is not None:
        vibration_parts.append(chakra_score)
        vibration_sources["chakras"] = chakra_score
    vibration_score = round(sum(vibration_parts) / len(vibration_parts), 1) if vibration_parts else None
    metrics["vibration"] = {"score": vibration_score, "sources": vibration_sources}

    # Recovery / Sleep metric
    metrics["sleep"] = {"score": sleep_score, "sources": {"sleep_quality_avg": sleep_quality_avg}}

    # Willpower / Resistance: cold showers (lower resistance is good), habit completion (if habits app exists)
    # Habits: compute completion rate if habits app exists
    try:
        from habits.models import Habit, HabitLog
        # For the period compute average completion rate across active habits
        habits = Habit.objects.filter(user=user)
        completion_rates = []
        for h in habits:
            total = h.logs.filter(date__range=(start, end)).count()
            done = h.logs.filter(date__range=(start, end), status="done").count()
            if total:
                completion_rates.append(done / total * 100)
        willpower_score = round(sum(completion_rates) / len(completion_rates), 1) if completion_rates else None
    except Exception:
        willpower_score = None

    willpower_sources = {}
    if cold_score is not None:
        willpower_sources["cold_showers"] = cold_score
    if willpower_score is not None:
        willpower_sources["habit_completion"] = willpower_score
    # average for willpower
    wp_parts = [v for v in [cold_score, willpower_score] if v is not None]
    willpower_final = round(sum(wp_parts) / len(wp_parts), 1) if wp_parts else None
    metrics["willpower"] = {"score": willpower_final, "sources": willpower_sources}

    # Compose some additional metrics such as focus/intution/perception by reusing existing data
    # For now, map focus <- meditation+workouts, intuition <- soulnotes+meditation, memory <- sleep
    metrics["focus"] = {
        "score": round(((clarity_score or 0) + (energy_score or 0)) / (2 if (clarity_score or energy_score) else 1), 1)
        if (clarity_score or energy_score) else None,
        "sources": {"clarity": clarity_score, "energy": energy_score}
    }

    metrics["intuition"] = {
        "score": round(((soulnotes_score or 0) + (med_clarity_score or 0)) / (2 if (soulnotes_score or med_clarity_score) else 1), 1)
        if (soulnotes_score or med_clarity_score) else None,
        "sources": {"soul_notes": soulnotes_score, "meditation": med_clarity_score}
    }

    metrics["memory"] = {"score": sleep_score, "sources": {"sleep_quality_avg": sleep_quality_avg}}

    # Return assembled dictionary
    summary = {
        "period": period,
        "start_date": str(start),
        "end_date": str(end),
        "metrics": metrics,
    }
    return summary
