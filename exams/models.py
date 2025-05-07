from django.db import models
from users.models import StudentProfile

class Course(models.Model):
    code = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.code
    
class Grade(models.Model):
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    midterm_grade = models.FloatField(null=True, blank=True)
    final_exam_grade = models.FloatField(null=True, blank=True) 
    final_grade = models.FloatField(null=True, blank=True)  # Numeric final grade
    letter_grade = models.CharField(max_length=2, null=True, blank=True)
    eligibility = models.CharField(max_length=50)
    absences = models.IntegerField(default=0) 
    declared_resit = models.BooleanField(default=False)
    # Resit-related fields
    resit_exam_grade = models.FloatField(null=True, blank=True)
    resit_final_grade = models.FloatField(null=True, blank=True)  # GPA from resit
    resit_letter_grade = models.CharField(max_length=2, null=True, blank=True)
    

    def __str__(self):
        return f"{self.student.user.email} - {self.course.code} - {self.letter_grade}"


