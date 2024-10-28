from django.db import models

from superadmin.models import Profile
from django.contrib.auth.models import User

STATUS_CHOICES = [
        ('Present', 'Present'),
        ('Absent', 'Absent'),
        ('Week Off', 'Week Off'),
    ]

class Attendance(models.Model):
    attendance_Id = models.AutoField(primary_key=True)
    profile = models.ForeignKey(Profile,on_delete=models.CASCADE)
    date = models.DateField()
    mark_attendance = models.CharField(max_length=20, choices=STATUS_CHOICES)
    login_time = models.TimeField(null=True, blank=True)
    logout_time = models.TimeField(null=True, blank=True)
    duration = models.CharField(max_length=10, null=True, blank=True)  
    created_on = models.DateField(auto_now_add=True)
    updated_on = models.DateField(auto_now=True)