from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    timetable_url = models.URLField(max_length=200)

    def __str__(self):
        return self.user.username