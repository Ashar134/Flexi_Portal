# teacherportal/urls.py
from django.urls import path
from teacherportal import views

urlpatterns = [
    path('teacherdashboard/', views.dashboard, name='teacherdashboard'),
    path('teachertimetable/', views.teacher_timetable, name='teacher_timetable'),
    path('teacherattendance/', views.attendance, name='attendance'),
    path('teacherattendance/detail/', views.attendance, name='attendance_detail'),  # New detail view
    path('teacherdiscussion/', views.discussion, name='discussion'),
    path('studentgrades/', views.student_grades, name='studentgrades'),
    path('classroom/', views.classroom, name='classroom'),
    path('download_resource/<int:resource_id>/', views.download_resource, name='download_resource'),
    path('give-marks/', views.give_marks, name='give_marks'),
    path('update-marks/', views.update_marks, name='update_marks'),


]

