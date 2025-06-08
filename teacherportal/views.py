from django.shortcuts import render , redirect
from django.contrib.auth.decorators import login_required
from datetime import datetime
from django.http import JsonResponse
from .models import  Attendance,Marks
from studentportal.models import Student
from .form import AttendanceForm
from django.utils import timezone
from django.utils.timezone import now
from .models import TeacherTimetable
from .models import Attendance, Teacher
from django.urls import reverse

from studentportal.models import Student
from django.contrib.auth.models import User
from django.http import FileResponse,HttpResponseRedirect
from django.shortcuts import get_object_or_404
from .models import Resource
from .form import ResourceUploadForm


# Teacher dashboard
def dashboard(request):
    # Get the current date
    current_date = datetime.now().strftime("%B %d, %Y")

    # Fetch the teacher object associated with the logged-in user
    teacher = Teacher.objects.get(user=request.user)

    context = {
        'current_date': current_date,
        'teacher': teacher,
    }
    
    return render(request, 'teacherdashboard.html', context)


# Teacher timetable
def teacher_timetable(request):
    # Fetch timetable for the logged-in teacher
    timetable = TeacherTimetable.objects.filter(teacher=request.user).order_by('day', 'time')
    return render(request, 'teachertimetable.html', {'timetable': timetable})

# Attendance
@login_required
def attendance(request):
    error_message = None  # Variable to store the error message
    
    try:
        # Get the teacher profile for the logged-in user
        teacher = request.user.teacher_profile
        students = teacher.get_students()  # Get students assigned to this teacher
        selected_date = request.POST.get('attendance_date', now().date())  # Default to today's date
        # Parse date if it's a string in 'Month DD, YYYY' format
        if isinstance(selected_date, str) and ',' in selected_date:
            try:
                selected_date = datetime.strptime(selected_date, '%B %d, %Y').date()
            except ValueError:
                pass  
        action = request.POST.get('action', 'mark')  # Default action is 'mark'

        if request.method == 'POST':
            if action == 'mark':
                # Render the form to mark attendance
                return render(
                    request,
                    'teacherattendance.html',
                    {'students': students, 'selected_date': selected_date, 'action': 'mark', 'error_message': error_message}
                )
            elif action == 'save':
                # Save attendance and associate the teacher who marked it
                for student in students:
                    attendance_status = request.POST.get(f'attendance_{student.id}')
                    if attendance_status is not None:
                        is_present = attendance_status in ['Present', 'Late']
                        remarks = "Late" if attendance_status == "Late" else ""
                        
                        # Update or create attendance with the teacher linked
                        Attendance.objects.update_or_create(
                            student=student,
                            date=selected_date,
                            defaults={
                                'is_present': is_present, 
                                'remarks': remarks,
                                'teacher': teacher  # Link the teacher to the attendance record
                            }
                        )
                return redirect('attendance')  # Redirect back to the attendance page after saving
            elif action == 'view':
                # Fetch attendance records for the selected date
                attendance_records = Attendance.objects.filter(student__in=students, date=selected_date)
                return render(
                    request,
                    'teacherattendance.html',
                    {'attendance_records': attendance_records, 'selected_date': selected_date, 'action': 'view', 'error_message': error_message}
                )

        # Default action (GET request) is 'mark' mode
        return render(
            request,
            'teacherattendance.html',
            {'students': students, 'selected_date': selected_date, 'action': 'mark', 'error_message': error_message}
        )
    except Teacher.DoesNotExist:
        # If the teacher is not assigned, show an error message on the same page
        error_message = 'You are not assigned as a teacher or have no students assigned to you.'
        return render(
            request,
            'teacherattendance.html',
            {'error_message': error_message}
        )
# attendance_detail
def attendance_detail(request):
    try:
        teacher = request.user.teacher_profile
        students = teacher.get_students()
        attendance_date = request.GET.get('date', timezone.now().date())  # Default to today
        attendance_records = Attendance.objects.filter(student__in=students, date=attendance_date)

        return render(
            request,
            'attendance_detail.html',
            {
                'attendance_records': attendance_records,
                'attendance_date': attendance_date,
                'students': students,
            }
        )
    except Teacher.DoesNotExist:
        return render(request, 'error.html', {'message': 'You are not assigned as a teacher.'})
    


def discussion(request):
    return render(request, 'teacherdiscussion.html')  


# Teacher mystudent
def student_grades(request):
    return render(request, 'studentgrades.html')  



# Teacher classroom
def classroom(request):
    if request.method == 'POST' and 'upload_resource' in request.POST:
        form = ResourceUploadForm(request.POST, request.FILES)
        if form.is_valid():
            resource = form.save(commit=False)
            resource.teacher = request.user  # Associate the uploaded resource with the logged-in teacher
            resource.save()
            return redirect('classroom')  # Redirect to the same page to avoid re-submitting the form
    else:
        form = ResourceUploadForm()

    # Fetch all resources uploaded by the logged-in teacher
    resources = Resource.objects.filter(teacher=request.user)

    return render(request, 'classroom.html', {'form': form, 'resources': resources})


def download_resource(request, resource_id):
    resource = get_object_or_404(Resource, id=resource_id)

    # Open the file in binary mode
    file_path = resource.file.path

    # Return the file as a response for download
    response = FileResponse(open(file_path, 'rb'), content_type='application/octet-stream')
    response['Content-Disposition'] = f'attachment; filename="{resource.title}"'  # Use the resource's title as the filename
    return response

@login_required
def give_marks(request):
    try:
        teacher = request.user.teacher_profile
        students = teacher.get_students()  # Get students linked to the teacher
        
        if request.method == 'POST':
            selected_date = request.POST.get('date_awarded', None)  # Get the date
            for student in students:
                marks = request.POST.get(f'marks_{student.id}')
                remarks = request.POST.get(f'remarks_{student.id}', '')

                if marks is not None and selected_date:
                    # Create or update the marks entry
                    Marks.objects.update_or_create(
                        teacher=teacher,
                        student=student,
                        date_awarded=selected_date,  # Use the specified date
                        defaults={'marks': marks, 'remarks': remarks}
                    )
            return redirect('give_marks')

        return render(request, 'give_marks.html', {'students': students})
    except Teacher.DoesNotExist:
        return render(request, {'message': 'You are not assigned as a teacher.'})

def update_marks(request):
    if request.method == "POST":
        teacher = Teacher.objects.get(user=request.user)
        date_awarded = request.POST.get('date_awarded')
        for student_id, marks in request.POST.items():
            if student_id.startswith("student_"):
                student_id = student_id.replace("student_", "")
                student = get_object_or_404(Student, id=student_id)
                marks_obj, created = Marks.objects.update_or_create(
                    teacher=teacher,
                    student=student,
                    date_awarded=date_awarded,
                    defaults={'marks': marks, 'remarks': request.POST.get(f"remarks_{student_id}", "")}
                )
        return HttpResponseRedirect(reverse('update_marks'))

    students = Student.objects.all()
    return render(request, 'update_marks.html', {
        'students': students,
        'current_date': datetime.now().date()
    })
