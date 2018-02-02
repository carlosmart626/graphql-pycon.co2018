from django.db import models
from django.contrib.auth.models import User


class Course(models.Model):
    title = models.CharField(max_length=150)
    description = models.TextField(max_length=500)
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, related_name='courses')
    is_active = models.BooleanField(default=True)
    enrolled_students = models.ManyToManyField(User, blank=True)

    def __str__(self):
        return f'{self.title}'
