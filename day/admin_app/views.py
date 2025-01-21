
from django.db.models import Avg, Sum
from django.shortcuts import render,redirect,get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import *
from django.contrib.auth import login, authenticate, update_session_auth_hash ,logout
from django.contrib.auth.decorators import login_required
import csv
from django.http import HttpResponse
import openpyxl
from .serializer import EventDataSerializer
from manager_app.models import Event_Data
from django.contrib import messages



# Create your views here.



def index(request):
    return render(request,'index.html ')


def Admin_Login(request):
    if request.method == 'POST':
        username = request.POST.get('admin_username')
        password = request.POST.get('admin_password')
        Admin_user = authenticate(request,username=username,password=password)
        if Admin_user is not None:
            login(request,Admin_user)
            return redirect('Admin_Dashboard')
        else:
            messages.error(request,"Invalid Username or Password")
            return redirect('Error-Page')

    return render(request,'index.html')

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
            phone = request.POST.get('add_phone')

            if password != confirm_password:
                return redirect('Admin-Signup')
            Admin_User = LoginSide.objects.create_user(username=username,first_name=first_name,last_name=last_name,photo=profile_img,password=password,email=Admin_email,login_role="Admin",phone_number=phone)
            Admin_User.save()

            return redirect('Admin_Login')
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
    total_user_data = LoginSide.objects.filter(login_role='Handler')
    total_user = total_user_data.count()

    total_impact_result = Event_Data.objects.aggregate(Sum('total_impact'))
    total_impact = total_impact_result['total_impact__sum'] if total_impact_result['total_impact__sum']is not None else 0
    impact_avg = Event_Data.objects.aggregate(Avg('total_impact'))
    avg_impact = impact_avg['total_impact__avg'] if impact_avg['total_impact__avg']is not None else 0
    contex = {
        'total_manager' :total_user,
        'total_event':total_event,
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




def error_page(request):
    return render(request,'Admin/components/Error_404.html')


from django.http import HttpResponse
import openpyxl

def download_excel(request):

    workbook = openpyxl.Workbook()
    sheet = workbook.active
    sheet.title = 'Event Data'


    headers = [
        'Event Date', 'Manager Name', 'Role YI', 'Project Verticals',
        'Project StackHolder', 'YI Pillar', 'SIG', 'Event Handle', 'Impact'
    ]
    sheet.append(headers)


    event_data = Event_Data.objects.all()
    for i in event_data:
        row = [
            i.date, i.your_name, i.role_yi, i.project_vertical,
            i.project_stakeholder, i.yi_pillar, i.which_SIG,
            i.event_handle, i.total_impact ]
        sheet.append(row)
    response = HttpResponse(
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    response['Content-Disposition'] = 'attachment; filename="Event_Data.xlsx"'

    workbook.save(response)
    return response

def manager_list(request):
    if request.user.login_role != 'Admin':
        return redirect('Error-Page')
    manager = LoginSide.objects.filter(login_role='Handler')
    contex = {
        'managers' :manager
    }
    return render(request,'Admin/view_manager.html',contex)


def delete_handler(request,handler_id):
    if request.user.login_role != 'Admin':
        return redirect('Error-Page')
    if request.method == 'POST':
        handler = get_object_or_404(LoginSide, id=handler_id)
        handler.delete()
    return redirect('View-manager')





def delete_event(request,event_id):
    if request.user.login_role != 'Admin':
        return redirect('Error-Page')
    if request.method == 'POST':
        delete_events = get_object_or_404(Event_Data,id=event_id)
        delete_events.delete()

    return redirect('Event_List')


def update_manager(request,manager_id):
    if request.user.login_role != 'Admin':
        return redirect('Error-Page')
    update_manager_data = get_object_or_404(LoginSide,id=manager_id)
    if request.method == 'POST':
        update_manager_data.first_name = request.POST['manager_first_name']
        update_manager_data.last_name = request.POST['manager_last_name']
        update_manager_data.username = request.POST['manager_username']
        update_manager_data.email = request.POST['manager_email']
        # update_manager_data.password = request.POST['manager_password']
        update_manager_data.phone_number = request.POST['manager_phone_number']
        if 'manager_profile_img' in request.FILES:
            update_manager_data.photo = request.FILES['manager_profile_img']
        update_manager_data.save()
    return redirect('View-manager')


def Email_side(request):
    return render(request,'Admin/Mail/mail.html')









class EventDataAPI(APIView):
    def get(self,request):
        event = Event_Data.objects.all()
        serializers = EventDataSerializer(event,many=True)
        return Response(serializers.data)












    




