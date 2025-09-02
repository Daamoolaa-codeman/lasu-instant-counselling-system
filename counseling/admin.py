from django.contrib import admin
from .models import Student, Counselor, Appointment, SessionRecord, Feedback, CounselingService,Video

@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ('title', 'youtube_url', 'date_added')

admin.site.register(Student)
admin.site.register(Counselor)
admin.site.register(CounselingService)
admin.site.register(Appointment)
admin.site.register(SessionRecord)
admin.site.register(Feedback)
