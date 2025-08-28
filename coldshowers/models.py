from django.db import models
from django.conf import settings
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.
class ColdShowerLog(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="cold_shower_logs"
    )
    mood_before = models.CharField(max_length=50)
    mood_after = models.CharField(max_length=50)
    resistance_level = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        default=5,
        help_text="Mental resistance level (1-10)"
    )
    duration_minutes = models.PositiveIntegerField(
        default=0,
        help_text="Duration of the shower in minutes"
    )
    water_temperature_celsius = models.DecimalField(
        max_digits=4,
        decimal_places=1,
        null=True,
        blank=True,
        help_text="Optional: water temperature in °C"
    )
    notes = models.TextField(blank=True, null=True)
    date = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ["-date"]
        verbose_name = "Cold Shower Log"
        verbose_name_plural = "Cold Shower Logs"

    def __str__(self):
        return f"{self.user.username} - {self.date.date()} - Resistance:{self.resistance_level}"

  

    