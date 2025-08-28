from django.db import models
from django.conf import settings
from django.utils import timezone

# Create your models here.
class SoulNote(models.Model):
    MOOD_CHOICES = [
        ('happy', 'Happy'),
        ('neutral', 'Neutral'),
        ('sad', 'Sad'),
        ('reflective', 'Reflective'),
        ('grateful', 'Grateful'),
        ('motivated', 'Motivated'),
        ('focused', 'Focused'),
        ('anxious', 'Anxious'),
        ('inspired', 'Inspired'),
        ('calm', 'Calm'),
        ('peaceful', 'Peaceful'),
        ('creative', 'Creative'),
        ('flow_state', 'Flow State'),
        ('energetic', 'Energetic'),
        ('spiritually_connected', 'Spiritually Connected'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="soul_notes"
    )
    title = models.CharField(max_length=200)
    content = models.TextField()
    tags = models.CharField(max_length=200, blank=True, null=True, help_text="Comma-separated tags")
    mood = models.CharField(max_length=50, choices=MOOD_CHOICES, blank=True, null=True)
    solfeggio_frequency = models.ForeignKey(
        'solfeggio.SolfeggioFrequency',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="soul_notes"
    )
    is_private = models.BooleanField(default=True)
    date_created = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-date_created"]
        verbose_name = "Soul Note"
        verbose_name_plural = "Soul Notes"

    def __str__(self):
        return f"{self.user.username} - {self.title} ({self.date_created.strftime('%Y-%m-%d')})"

    def tag_list(self):
        if self.tags:
            return [tag.strip() for tag in self.tags.split(",")]
        return []
