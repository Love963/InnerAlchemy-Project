from django.db import models
from django.conf import settings
from django.utils import timezone

# Create your models here.

class SleepLog(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="sleep_logs")
    date = models.DateField(default=timezone.now)
    sleep_start = models.DateTimeField()
    sleep_end = models.DateTimeField()
    total_duration = models.DurationField(blank=True, null=True)
    quality_score = models.IntegerField(choices=[(i, str(i)) for i in range(1, 11)], default=5)
    mood_after = models.CharField(max_length=50, blank=True, null=True)
    rituals = models.TextField(blank=True, null=True, help_text="Bedtime rituals or practices")
    dream_notes = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ["-date"]
        indexes = [
            models.Index(fields=["user", "date"]),
        ]

    def __str__(self):
        return f"{self.user.username} - {self.date}"

    def save(self, *args, **kwargs):
        if self.sleep_start and self.sleep_end:
            self.total_duration = self.sleep_end - self.sleep_start
            self.date = self.sleep_start.date() 
        super().save(*args, **kwargs)

    def formatted_duration(self):
        if self.total_duration:
            hours, remainder = divmod(self.total_duration.seconds, 3600)
            minutes = remainder // 60
            return f"{hours}h {minutes}m"
        return "N/A"


class SleepStageType(models.Model):
    name = models.CharField(max_length=50)  
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class SleepStage(models.Model):
    sleep_log = models.ForeignKey(SleepLog, on_delete=models.CASCADE, related_name="stages")
    stage_type = models.ForeignKey(SleepStageType, on_delete=models.CASCADE)
    duration_minutes = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.stage_type.name} - {self.duration_minutes} min"

class SleepSolfeggioRecommendation(models.Model):
    sleep_log = models.ForeignKey(SleepLog, on_delete=models.CASCADE, related_name="solfeggio_recommendations")
    frequency = models.ForeignKey(
        "solfeggio.SolfeggioFrequency",
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    reason = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.sleep_log.user.username} - {self.frequency}"

