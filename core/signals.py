from django.db.models.signals import post_save
from django.dispatch import receiver
from breathwork.models import BreathworkSession
from coldshowers.models import ColdShowerLog
from sleep.models import SleepLog
from habits.models import Habit, HabitLog
from django.utils import timezone


def get_or_create_habit(user, name, frequency="daily"):
    """Utility: auto-create habit if not exists."""
    habit, created = Habit.objects.get_or_create(
        user=user,
        name=name,
        defaults={"frequency": frequency, "description": f"Auto-tracked habit for {name}"}
    )
    return habit


@receiver(post_save, sender=BreathworkSession)
def create_breathwork_habit_log(sender, instance, created, **kwargs):
    if created:
        habit = get_or_create_habit(instance.user, "Breathwork Practice", "daily")
        HabitLog.objects.get_or_create(
            habit=habit,
            date=timezone.now().date(),
            defaults={"status": "done", "notes": f"Session: {instance.technique}"}
        )


@receiver(post_save, sender=ColdShowerLog)
def create_coldshower_habit_log(sender, instance, created, **kwargs):
    if created:
        habit = get_or_create_habit(instance.user, "Cold Shower", "daily")
        HabitLog.objects.get_or_create(
            habit=habit,
            date=timezone.now().date(),
            defaults={"status": "done", "notes": f"Duration: {instance.duration} min"}
        )


@receiver(post_save, sender=SleepLog)
def create_sleep_habit_log(sender, instance, created, **kwargs):
    if created:
        habit = get_or_create_habit(instance.user, "Healthy Sleep", "daily")
        HabitLog.objects.get_or_create(
            habit=habit,
            date=instance.sleep_start.date(),
            defaults={"status": "done", "notes": f"Duration: {instance.total_duration}"}
        )
