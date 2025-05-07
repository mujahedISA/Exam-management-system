from django.db import models

from exams.models import Course

class ResitExamSchedule(models.Model):
    course = models.OneToOneField(Course, on_delete=models.CASCADE)
    place = models.CharField(max_length=100)
    date = models.CharField(max_length=100)  # or DateField if it's always a date

class ResitExamContent(models.Model):
    course = models.OneToOneField(Course, on_delete=models.CASCADE)
    exam_type = models.CharField(max_length=50)
    num_questions = models.PositiveIntegerField()
    calculator_allowed = models.BooleanField(default=False)
    additional_notes = models.TextField(blank=True)