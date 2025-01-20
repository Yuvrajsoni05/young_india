
from django.db.models import Avg, Sum
from django.shortcuts import render,redirect,get_object_or_404
from .models import *
from django.contrib.auth import login, authenticate, update_session_auth_hash ,logout
from django.contrib.auth.decorators import login_required
import csv
from django.http import HttpResponse
import openpyxl

# from ..manager_app.views import event_list
from manager_app.models import Event_Data

# from ..manager_app.views import event_data


# Create your views here.

def Admin_Login(request):
    if request.method == 'POST':
        username = request.POST.get('admin_username')
        password = request.POST.get('admin_password')
        Admin_user = authenticate(request,username=username,password=password)

        login(request,Admin_user)
            # return HttpResponse("Yuvraj Soni")
        return redirect('Admin_Dashboard')

    # else:
    #     return redirect('Error-Page')

    return render(request,'Admin/AdminLogin.html')

@login_required(login_url='Admin_Login')
def Admin_Signup(request):
    if request.user.login_role != 'Admin':
        return redirect('Error-Page')
    else:
        if request.method == 'POST':
            username = request.POST.get('add_username')
            first_name = request.POST.get('fist_name')
            last_name = request.POST.get('last_name')
            password = request.POST.get('password1')
            profile_img = request.FILES.get('profile_img')
            confirm_password = request.POST.get('password2')
            Admin_email = request.POST.get('add_email')

            if password != confirm_password:
                return redirect('Admin-Signup')
            Admin_User = LoginSide.objects.create_user(username=username,first_name=first_name,last_name=last_name,photo=profile_img,password=password,email=Admin_email,login_role="Admin")
            Admin_User.save()
            login(request,Admin_User)
            return redirect('Admin_Dashboard')
    return render(request,'Admin/AdminSignup.html')

@login_required(login_url='Admin_Login')
def Admin_Profile(request):
    if request.user.login_role != 'Admin':
        return redirect('Error-Page')
    # else:
    #     return redirect('Admin_Profile')
    return render(request, 'Admin/Admin_Profile.html')


@login_required(login_url='Admin_Login')
def Admin_update(request,admin_id):
    if request.user.login_role != "Admin":
        return redirect('Error-Page')
    else:
        if request.user.login_role == "Admin":
            if request.method == 'POST':
                admin_profile = get_object_or_404(LoginSide,id=admin_id)
                admin_profile.first_name = request.POST['admin_firstname']
                admin_profile.last_name = request.POST['admin_lastname']
                admin_profile.email = request.POST['admin_email']
                # admin_profile.photo = request.FILES['admin_profile_img']
                admin_profile.username = request.POST['admin_username']
                admin_profile.phone_number = request.POST['admin_phone']
                if 'admin_profile_img' in request.FILES:
                    admin_profile.photo = request.FILES['admin_profile_img']
                admin_profile.save()
                return redirect('Admin_Profile')
    # return render(request,'Admin/Admin_Profile.html')


@login_required(login_url='Admin_Login')
def admin_password(request):
    if request.user.login_role == "Admin":
        if request.method == 'POST':
            old_password = request.POST.get('old_password')
            new_password = request.POST.get('new_password')
            confirm_password = request.POST.get('confirm_password')
            admin_user =request.user
            if not admin_user.check_password(old_password):
                return redirect('Admin_dashboard')
            if new_password != confirm_password:
                return redirect('Admin_dashboard')

            admin_user.set_password(new_password)
            admin_user.save()
            update_session_auth_hash(request,admin_user)
            return redirect('Admin_Profile')
        else:
            return redirect('Error-Page')


@login_required(login_url='Admin_Login')
def admin_logout(request):
    logout(request)
    return redirect('Admin_Login')


@login_required(login_url='Admin_Login')
def Admin_Dashboard(request):
    if request.user.login_role != 'Admin':
        return redirect('Error-Page')
    total_event = Event_Data.objects.count()
    total_impact_result = Event_Data.objects.aggregate(Sum('total_impact'))
    total_impact = total_impact_result['total_impact__sum'] if total_impact_result['total_impact__sum']is not None else 0
    impact_avg = Event_Data.objects.aggregate(Avg('total_impact'))
    avg_impact = impact_avg['total_impact__avg'] if impact_avg['total_impact__avg']is not None else 0
    contex = {
        'total':total_event,
        'total_impact':total_impact,
        'impact_avg':avg_impact,
    }
    return render(request, 'Admin/AdminDashboard.html',contex)


@login_required(login_url='Admin_Login')
def Event_list(request):
    if request.user.login_role != 'Admin':
        return redirect('Error-Page')

    event_list = Event_Data.objects.all()
    context = {
        'events' : event_list
    }
    return render(request,'Admin/event_list.html',context)



@login_required(login_url='Admin_Login')
def error_page(request):
    return render(request,'Admin/components/Error_404.html')


def download_excel(request):
    workbook = openpyxl.Workbook()
    sheet = workbook.active
    sheet.title = 'Event Data'
    headers = ['Event Date','Manager Name','Role YI','Project Verticals','Project StackHolder','YI Pillar','SIG','Event Handle','Impact']
    sheet.append(headers)

    event_data = Event_Data.objects.all()
    for i in event_data:
        row = [i.date,i.your_name,i.role_yi,i.project_vertical,i.project_stakeholder,i.yi_pillar,i.which_SIG,i.event_handle,i.total_impact]
        sheet.append(row)
    response = HttpResponse(content_type="application/vnd.openxmlformats-officedoucment.spreadsheetml.sheet")
    response['Content-Disposition'] = 'attachment; filename="Event Data.xlsx" '
    workbook.save(response)
    return response


def delete_multiple(request,id=None):
    if request.method == 'POST':
        get_id = request.POST.getlist('delete_data')

        for getid in get_id:
            event_data = Event_Data.objects.get(id=getid)
            event_data.delete()

    return redirect('Event_List')

def manager_list(request):
    manager = LoginSide.objects.filter(login_role='Handler')
    contex = {
        'managers' :manager
    }
    return render(request,'Admin/view_manager.html',contex)





    




