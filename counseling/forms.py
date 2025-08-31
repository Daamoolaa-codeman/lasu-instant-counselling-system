from django import forms
from .models import Appointment
from .models import Feedback
from django import forms
from django.contrib.auth.models import User
from .models import Student, Counselor

class StudentSignupForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Student
        fields = ['matric_no', 'faculty', 'department']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['matric_no'].widget.attrs.update({'placeholder': 'Matriculation Number'})
        self.fields['faculty'].widget.attrs.update({'placeholder': 'Faculty'})
        self.fields['department'].widget.attrs.update({'placeholder': 'Department'})

class CounselorSignupForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Counselor
        fields = ['specialization', 'office_location']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['specialization'].widget.attrs.update({'placeholder': 'Specialization'})
        self.fields['office_location'].widget.attrs.update({'placeholder': 'Office Location'})

class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['counseling_service', 'date', 'time']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['counseling_service'].empty_label = "--- Select a Counseling Service ---"

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['rating', 'comments']
        widgets = {
            'rating': forms.NumberInput(attrs={'min': 1, 'max': 5}),
            'comments': forms.Textarea(attrs={'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        student = kwargs.pop('student', None)
        super().__init__(*args, **kwargs)
        if student:
            self.fields['appointment'].queryset = Feedback.objects.none()
            self.fields['appointment'].queryset = student.appointment_set.filter(feedback__isnull=True)
