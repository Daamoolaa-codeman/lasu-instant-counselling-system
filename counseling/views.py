from django.shortcuts import render, redirect
from .models import Appointment, Student
from .forms import AppointmentForm  
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .models import Appointment
from .models import Student
from .forms import FeedbackForm
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from .forms import StudentSignupForm, CounselorSignupForm
from .models import Student, Counselor, CounselingService
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Appointment, Feedback
from .models import Video

def video_list(request):
    videos = Video.objects.all().order_by('-date_added')
    return render(request, 'videos/video_list.html', {'videos': videos})



@login_required 
def counselor_dashboard(request):
    counselor = request.user.counselor
    completed_sessions = Appointment.objects.filter(counselor=counselor, status='Completed').count()

    context = {
        'completed_sessions': completed_sessions,
        'role': "counselor"
    }

    return render(request, 'counseling/counselor_dashboard.html', context)


@login_required
def student_dashboard(request):
    student = request.user.student
    total_appointments = Appointment.objects.filter(student=student).count()
    completed_sessions = Appointment.objects.filter(student=student, status='completed').count()
    pending_appointments = Appointment.objects.filter(student=student, status='pending').count()

    return render(request, 'counseling/student_dashboard.html', {
        'total_appointments': total_appointments,
        'completed_sessions': completed_sessions,
        'pending_appointments': pending_appointments,
        'role': "student"
    })


def about_counseling(request):
    return render(request, 'counseling/about_counseling.html')


def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect('/')  # or a landing page



def student_login(request):
    if request.method == 'POST':
        matric_no = request.POST['matric_no']
        password = request.POST['password']
        user = authenticate(request, username=matric_no, password=password)
        if user is not None and hasattr(user, 'student'):
            login(request, user)
            return redirect('student_dashboard')  # or 'student_dashboard'
        else:
            messages.error(request, 'Invalid credentials or not a student.')
    return render(request, 'counseling/student_login.html')

def counselor_login(request):
    if request.method == 'POST':
        pf_number = request.POST['pf_number']
        password = request.POST['password']
        print(pf_number, password)
        user = authenticate(request, username=pf_number, password=password)
        if user is not None and hasattr(user, 'counselor'):
            login(request, user)
            return redirect('counselor_dashboard')
        else:
            messages.error(request, 'Invalid credentials or not a counselor.')
    return render(request, 'counseling/counselor_login.html')


def student_signup(request):
    if request.method == 'POST':
        user = User.objects.create_user(
            username=request.POST['matric_no'],
            password=request.POST['password'],
            first_name=request.POST.get('first_name', ''),
            last_name=request.POST.get('last_name', '')
        )
        student_form = StudentSignupForm(request.POST)
        if student_form.is_valid():
            student = student_form.save(commit=False)
            student.user = user
            student.save()
            login(request, user)
            messages.success(request, 'Student account created successfully.')
            return redirect('book_appointment')
    else:
        student_form = StudentSignupForm()
    return render(request, 'counseling/student_signup.html', {'form': student_form})

def counselor_signup(request):
    if request.method == 'POST':
        user = User.objects.create_user(
            username=request.POST['pf_number'],
            password=request.POST['password'],
            first_name=request.POST.get('first_name', ''),
            last_name=request.POST.get('last_name', ''),
            email=request.POST.get('email', '')
        )
        counselor_form = CounselorSignupForm(request.POST)
        if counselor_form.is_valid():
            counselor = counselor_form.save(commit=False)
            counselor.user = user
            counselor.save()
            login(request, user)
            messages.success(request, 'Counselor account created successfully.')
            return redirect('counselor_dashboard')
    else:
        counselor_form = CounselorSignupForm()
    return render(request, 'counseling/counselor_signup.html', {'form': counselor_form})


@login_required
def submit_feedback(request, appointment_id):
    appointment = Appointment.objects.get(id=appointment_id)

    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.student = request.user.student
            feedback.appointment = appointment
            feedback.save()
            messages.success(request, "Thank you! Your feedback has been submitted.")
            return redirect('view_appointments')
    else:
        form = FeedbackForm()

    return render(request, 'counseling/submit_feedback.html', {'form': form, 'appointment': None})


@login_required
def book_appointment(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            # Fetch the Student instance linked to the user
            # CounselingService.objects.get(id=1).get_preferred_counselor()
            appointment.student = Student.objects.get(user=request.user)
            counseling_service_id = form.data["counseling_service"]
            appointment.counselor = CounselingService.objects.get(id=counseling_service_id).get_preferred_counselor()
            appointment.save()

            # Send an email to the counselor
            counselor_email_address = appointment.counselor.get_email_address()

            print(counselor_email_address)

            return redirect('appointment_success')
    else:
        form = AppointmentForm()

    return render(request, 'counseling/book_appointment.html', {'form': form})




@login_required
def view_appointment(request):
    student = Student.objects.get(user=request.user)
    appointments = Appointment.objects.filter(student=student)
    return render(request, 'counseling/view_appointments.html', {'appointments': appointments})

@login_required
def appointment_success(request):
    return render(request, 'counseling/appointment_success.html')


def students_feedback(request):
    return render(request, 'counseling/students_feedback.html')

def render_homepage(request):
    return render(request, 'counseling/homepage.html')

def render_session_history(request):
    return render(request, 'counseling/session_history.html')