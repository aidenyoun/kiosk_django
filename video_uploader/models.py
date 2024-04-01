# video_uploader/models.py
from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    heart_rate = models.CharField(max_length=20)
    respiration_rate = models.CharField(max_length=20)
    stress_score = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s profile"
