from django.db import models
from django.contrib.auth.models import User


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    matric_no = models.CharField(max_length=20, unique=True)
    faculty = models.CharField(max_length=100)
    department = models.CharField(max_length=100)

    def __str__(self):
        return self.user.get_full_name()

class Counselor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    specialization = models.CharField(max_length=100)
    office_location = models.CharField(max_length=100)

    def __str__(self):
        return self.user.get_full_name()
    
    def get_email_address(self):
        return self.user.email
    
class CounselingService(models.Model):
    counselors = models.ManyToManyField("Counselor", related_name="services")
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
    def get_preferred_counselor(self):
        return self.counselors.first()

class Appointment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    counselor = models.ForeignKey(Counselor, on_delete=models.CASCADE)
    counseling_service = models.ForeignKey(CounselingService, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    status = models.CharField(max_length=20, choices=[('Pending', 'Pending'), ('Completed', 'Completed')], default='Pending')

    def __str__(self):
        return f"{self.student.user.get_full_name()} with {self.counselor.user.get_full_name()}"

class SessionRecord(models.Model):
    appointment = models.OneToOneField(Appointment, on_delete=models.CASCADE)
    notes = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class Feedback(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE)
    rating = models.IntegerField()
    comments = models.TextField(blank=True, null=True)
    submitted_at = models.DateTimeField(auto_now_add=True)
