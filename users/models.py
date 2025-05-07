from django.db import models

from django.contrib.auth.models import User


class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    program = models.CharField(max_length=100)
    generated_password = models.CharField(max_length=100, blank=True, null=True)  
    def __str__(self):
        return self.user.email

