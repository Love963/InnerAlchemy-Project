from django.db import models
from django.db import models
from django.contrib.auth import get_user_model
# Create your models here.

User = get_user_model()

class UserActivity(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='activities')
    app_name = models.CharField(max_length=100)
    action = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.app_name} - {self.action}"
