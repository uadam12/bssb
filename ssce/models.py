from django.db import models
from users.models import User
from applicant.models import SchoolAttended

# Create your models here.
class SSCE(models.Model):
    TYPES = (('waec', 'WAEC'), )

    exam_number = models.CharField(max_length=20)
    serial_number = models.CharField(max_length=15)
    graduation_year = models.SmallIntegerField()
    ssce_type =models.CharField(max_length=15, choices=TYPES)
    candidate = models.ForeignKey(User, on_delete=models.CASCADE)
    school = models.ForeignKey(SchoolAttended, on_delete=models.CASCADE, related_name='ssces')
    
    def get_percentage(self, *subject_ids):
        return len(subject_ids)
    
    def __str__(self):
        return f"{self.ssce_type.upper()} of {self.candidate} - {self.graduation_year}"

class Subject(models.Model):
    name = models.CharField(max_length=50, unique=True)
    is_compulsory = models.BooleanField(default=False)
    
    def __str__(self):
        return self.name


class Grade(models.Model):
    name = models.CharField(max_length=3, unique=True)
    value = models.PositiveSmallIntegerField(default=0, unique=True)
    
    def __str__(self):
        return self.name

    
class Record(models.Model):
    ssce = models.ForeignKey(SSCE, on_delete=models.CASCADE, related_name='records')
    grade = models.ForeignKey(Grade, on_delete=models.CASCADE, related_name='records')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='records')

    def __str__(self):
        return f"{self.subject}: {self.grade}"