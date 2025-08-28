from django.db import models
from django.conf import settings
from django.utils import timezone
from django.utils.text import slugify

# Create your models here.
class Tag(models.Model):
    # tag model for categorizing affirmations.
    name = models.CharField(max_length=50, unique=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class VisualizationAffirmation(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = models.TextField()

    # Tags can now be structured via ManyToMany
    tags = models.ManyToManyField(Tag, related_name="affirmations", blank=True)

    solfeggio_frequency = models.ForeignKey(
        'solfeggio.SolfeggioFrequency',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="affirmations"
    )

    slug = models.SlugField(max_length=220, unique=True, blank=True)

    date_created = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date_created']
        verbose_name = "Affirmation"
        verbose_name_plural = "Affirmations"

    def save(self, *args, **kwargs):
        if not self.slug:
            # Slug includes user + first part of title for uniqueness
            self.slug = slugify(f"{self.user.username}-{self.title[:50]}")
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title[:30]}... by {self.user.username}"
