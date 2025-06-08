from django.contrib import admin
from .models import TeacherTimetable,Teacher,Attendance,Marks,Resource

class TeacherAdmin(admin.ModelAdmin):
    llist_display = ('user', 'subject', 'qualification', 'date_of_birth', 'hire_date')
    list_filter = ('subject', 'qualification')
    search_fields = ('user__username', 'user__first_name', 'user__last_name')
    filter_horizontal = ('students',)

admin.site.register(Teacher, TeacherAdmin)
# Admin configuration for TeacherTimetable
@admin.register(TeacherTimetable)
class TeacherTimetableAdmin(admin.ModelAdmin):
    list_display = ('teacher', 'day', 'time', 'subject', 'location')  # Fields to display in the admin list view
    list_filter = ('day', 'teacher')  # Fields for filtering in the sidebar
    search_fields = ('teacher__username', 'subject')  # Fields for searching in the admin panel

    def __str__(self):  
        return f"{self.teacher.username} - {self.day} - {self.subject}"


# Register Discussion model

class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('student', 'date', 'is_present', 'remarks')
    list_filter = ('date', 'is_present')  # Filters by date and attendance status
    search_fields = ('student__user__first_name', 'student__user__last_name')  # Search by student name

    def get_queryset(self, request):
        # Display a combined view for the Attendance table
        return super().get_queryset(request).select_related('student', 'student__user')

admin.site.register(Attendance, AttendanceAdmin)
  # Ensure Student is registered as well
  
  


class ResourceAdmin(admin.ModelAdmin):
    list_display = ('teacher', 'title', 'description', 'file', 'uploaded_at')  # Fields to display in the list view
    search_fields = ('title', 'teacher__username')  # Fields to search in the admin panel
    list_filter = ('teacher', 'uploaded_at')  # Filters to narrow down the results
    ordering = ('-uploaded_at',)  # Order by the most recent uploaded resources

admin.site.register(Resource, ResourceAdmin)

class MarksAdmin(admin.ModelAdmin):
    list_display = ('teacher', 'student', 'marks', 'date_awarded', 'remarks')  # Display these fields in the admin list
    list_filter = ('date_awarded', 'teacher')  # Filters for date and teacher
    search_fields = ('student__user__first_name', 'student__user__last_name', 'teacher__user__username')  # Search functionality

    def get_queryset(self, request):
        """Optimize queryset to reduce database hits."""
        return super().get_queryset(request).select_related('teacher', 'student', 'student__user')

admin.site.register(Marks, MarksAdmin)
