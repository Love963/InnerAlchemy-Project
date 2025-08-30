from django.db import models
from django.conf import settings
from django.utils import timezone
from django.core.exceptions import ValidationError

# Create your models here.

class NutritionLog(models.Model):
    # Constants for meal choices 
    BREAKFAST = "breakfast"
    LUNCH = "lunch"
    DINNER = "dinner"
    SNACK = "snack"

    MEAL_CHOICES = [
        (BREAKFAST, "Breakfast"),
        (LUNCH, "Lunch"),
        (DINNER, "Dinner"),
        (SNACK, "Snack"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="nutrition_logs"
    )

    meal_type = models.CharField(max_length=10, choices=MEAL_CHOICES)
    food_items = models.TextField(help_text="List the foods consumed in this meal")
    calories = models.PositiveIntegerField(help_text="Total calories consumed")
    hydration_liters = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0,
        help_text="Liters of water consumed"
    )
    supplements = models.TextField(
        blank=True,
        null=True,
        help_text="Any supplements taken"
    )
    energy_effect = models.IntegerField(
        choices=[(i, str(i)) for i in range(1, 11)],
        default=5,
        help_text="How energized did you feel after eating? (1-10)"
    )
    mood_effect = models.IntegerField(
        choices=[(i, str(i)) for i in range(1, 11)],
        default=5,
        help_text="Mood change after eating (1-10)"
    )

    notes = models.TextField(blank=True, null=True)
    date = models.DateField(default=timezone.now)

    class Meta:
        ordering = ["-date"]
        indexes = [
            models.Index(fields=["user", "date"]),
        ]
        constraints = [
            models.UniqueConstraint(
                fields=["user", "meal_type", "date"],
                name="unique_meal_per_day"
            )
        ]

    # Validation
    def clean(self):
        if self.calories < 0:
            raise ValidationError("Calories cannot be negative.")
        if self.hydration_liters < 0:
            raise ValidationError("Hydration cannot be negative.")
        if not (1 <= self.energy_effect <= 10):
            raise ValidationError("Energy effect must be between 1 and 10.")
        if not (1 <= self.mood_effect <= 10):
            raise ValidationError("Mood effect must be between 1 and 10.")

    @property
    def nutrition_score(self):
        # Combine energy and mood effect into a simple score.
        return round((self.energy_effect + self.mood_effect) / 2, 1)

    def __str__(self):
        return (
            f"{self.user.username} - {self.get_meal_type_display()} "
            f"on {self.date} | {self.calories} kcal | Score: {self.nutrition_score}"
        )
