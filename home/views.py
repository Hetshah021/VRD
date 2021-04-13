from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User, auth
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.urls import reverse, reverse_lazy
from django.views.generic import DetailView
from django.views.generic.edit import UpdateView
from django.contrib.auth import authenticate, login, logout
from home.forms import RegisterForm, ChangePasswordForm
from home.models import MyUser, CameraDetails, VehicleDetails
# from django.core.files.storage import FileSystemStorage
from django.db import connection
from home.models import vehicle_details

def index(request):
    logout(request)
    return render(request, 'index.html')

def user_login(request):
    context = {}
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            if request.GET.get('next', None):
                return HttpResponseRedirect(request.GET['next'])
            return HttpResponseRedirect(reverse('home'))
        else:
            context['error'] = "Provide valid credentials !!"
            return render(request, "login.html", context)
    else:
        return render(request, 'login.html', context)

@login_required(login_url="user_login")
def home(request):
    camera_details = CameraDetails.objects.all()
    return render(request, 'dashboard.html', {'camera_details': camera_details})

@login_required(login_url="user_login")
def search(request):

    camera_details = CameraDetails.objects.raw(
        "select * from home_cameradetails GROUP BY location")

    # ---------- After Submitting From -----------
    if request.method == 'POST':
        if request.POST['vehicle_no']:
            vehicle_no = request.POST['vehicle_no']
        else:
            vehicle_no = None
        if request.POST['search_date']:
            date = request.POST['search_date']
        else:
            date = None
        if request.POST['location']:
            location = request.POST['location']
        else:
            location = "all"

        cursor = connection.cursor()
        if vehicle_no is None:
            if date is None:
                cursor.execute(
                    "SELECT home_vehicledetails.vehicle_no, home_cameradetails.location, home_vehicledetails.cameranum_id, home_vehicledetails.date, home_vehicledetails.time FROM home_vehicledetails "
                    "JOIN home_cameradetails ON home_vehicledetails.cameranum_id=home_cameradetails.cameranum WHERE home_cameradetails.location=%s",
                    [location])
                vehicle_details = cursor.fetchall()
            elif location == 'all':
                cursor.execute(
                    "SELECT home_vehicledetails.vehicle_no, home_cameradetails.location, home_vehicledetails.cameranum_id, home_vehicledetails.date, home_vehicledetails.time FROM home_vehicledetails "
                    "JOIN home_cameradetails ON home_vehicledetails.cameranum_id=home_cameradetails.cameranum WHERE home_vehicledetails.date=%s",
                    [date])
                vehicle_details = cursor.fetchall()
            else:
                cursor.execute(
                    "SELECT home_vehicledetails.vehicle_no, home_cameradetails.location, home_vehicledetails.cameranum_id, home_vehicledetails.date, home_vehicledetails.time FROM home_vehicledetails "
                    "JOIN home_cameradetails ON home_vehicledetails.cameranum_id=home_cameradetails.cameranum WHERE home_vehicledetails.date=%s AND home_cameradetails.location=%s",
                    [date, location])
                vehicle_details = cursor.fetchall()
        elif date is None:
            if location == 'all':
                cursor.execute(
                    "SELECT home_vehicledetails.vehicle_no, home_cameradetails.location, home_vehicledetails.cameranum_id, home_vehicledetails.date, home_vehicledetails.time FROM home_vehicledetails "
                    "JOIN home_cameradetails ON home_vehicledetails.cameranum_id=home_cameradetails.cameranum WHERE home_vehicledetails.vehicle_no=%s",
                    [vehicle_no])
                vehicle_details = cursor.fetchall()
            else:
                cursor.execute(
                    "SELECT home_vehicledetails.vehicle_no, home_cameradetails.location, home_vehicledetails.cameranum_id, home_vehicledetails.date, home_vehicledetails.time FROM home_vehicledetails "
                    "JOIN home_cameradetails ON home_vehicledetails.cameranum_id=home_cameradetails.cameranum WHERE home_vehicledetails.vehicle_no=%s AND home_cameradetails.location=%s", [vehicle_no, location])
                vehicle_details = cursor.fetchall()
        elif location == 'all':
            cursor.execute(
                "SELECT home_vehicledetails.vehicle_no, home_cameradetails.location, home_vehicledetails.cameranum_id, home_vehicledetails.date, home_vehicledetails.time FROM home_vehicledetails "
                "JOIN home_cameradetails ON home_vehicledetails.cameranum_id=home_cameradetails.cameranum WHERE home_vehicledetails.vehicle_no=%s AND home_vehicledetails.date=%s",
                [vehicle_no, date])
            vehicle_details = cursor.fetchall()
        else:
            cursor.execute(
                "SELECT home_vehicledetails.vehicle_no, home_cameradetails.location, home_vehicledetails.cameranum_id, home_vehicledetails.date, home_vehicledetails.time FROM home_vehicledetails "
                "JOIN home_cameradetails ON home_vehicledetails.cameranum_id=home_cameradetails.cameranum WHERE home_vehicledetails.vehicle_no=%s AND home_vehicledetails.date=%s AND home_cameradetails.location=%s",
                [vehicle_no, date, location])
            vehicle_details = cursor.fetchall()
        return render(request, 'search_dashboard.html', {'camera_details': camera_details,
             'vehicle_details': vehicle_details, 'vehicle_no': vehicle_no, 'date': date, 'location': location})


    # --------- Before Submitting From -----------
    else:
        cursor = connection.cursor()
        cursor.execute(
            "SELECT home_vehicledetails.vehicle_no, home_cameradetails.location, home_vehicledetails.cameranum_id, home_vehicledetails.date, home_vehicledetails.time FROM home_vehicledetails JOIN home_cameradetails ON home_vehicledetails.cameranum_id=home_cameradetails.cameranum ")
        vehicle_details = cursor.fetchall()
        return render(request, 'search_dashboard.html',
                      {'camera_details': camera_details, 'vehicle_details': vehicle_details})

@login_required(login_url="user_login")
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))

# def forget(request):
#     return render(request, 'forget.html')

class profile(DetailView):
    template_name = 'profile.html'

    @method_decorator(login_required(login_url='user_login'))
    def dispatch(self, *args, **kwargs):
        return super(profile, self).dispatch(*args, **kwargs)

    def get_object(self):
        return self.request.user

@login_required(login_url="user_login")
def profile_update(request, id=None):
    user = get_object_or_404(MyUser, id=id)
    if request.method == 'POST':
        register_form = RegisterForm(request.POST, instance=user)
        if register_form.is_valid():
            register_form.save()
            return HttpResponseRedirect(reverse('profile'))
        else:
            return render(request, 'editProfile.html', {"register_form": register_form})
    else:
        register_form = RegisterForm(instance=user)
        return render(request, 'editProfile.html', {"register_form": register_form})

@login_required(login_url="user_login")
def change_password(request, id=None):
    user = get_object_or_404(MyUser, id=id)
    if request.method == 'POST':
        change_password_form = ChangePasswordForm(request.POST, instance=user)
        if change_password_form.is_valid():
            change_password_form.save()
            return HttpResponseRedirect(reverse('profile'))
        else:
            return render(request, 'changePassword.html', {"change_password_form": change_password_form})
    else:
        change_password_form = ChangePasswordForm(instance=user)
        return render(request, 'changePassword.html', {"change_password_form": change_password_form})