from django.contrib import admin
from .models import Student, Counselor, Appointment, SessionRecord, Feedback, CounselingService

admin.site.register(Student)
admin.site.register(Counselor)
admin.site.register(CounselingService)
admin.site.register(Appointment)
admin.site.register(SessionRecord)
admin.site.register(Feedback)
