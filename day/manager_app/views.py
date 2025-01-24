from io import BytesIO

from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import login,authenticate,logout,update_session_auth_hash
from admin_app.models import LoginSide
from matplotlib import pyplot as plt
import matplotlib
import numpy as np
from .models import Event_Data
from  django.contrib.auth.decorators import login_required


# Create your views here.


def manager_login(request):
    if request.method == 'POST':
        username = request.POST.get('manager_username')
        password = request.POST.get('manager_password')
        manager_user = authenticate(request,username=username,password=password)
        if manager_user is not None and manager_user.login_role == 'Handler':
            login(request,manager_user)
            return redirect('manager-dashboard')
        else:
            messages.error(request,"Incorrect Username Password")
            return redirect('Error-Page')
    return render(request,'index.html')






@login_required(login_url='Admin_Login')
def manager_signup(request):
    if request.method == "POST":
        manager_username = request.POST.get('manager_username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        password = request.POST.get('password1')
        phone = request.POST.get('add_phone')
        profile_img = request.FILES.get('profile_img')
        confirm_password = request.POST.get('password2')
        manager_email = request.POST.get('manager_email')

        if len(phone) != 10 or not phone.isdigit():
            messages.error(request, "Phone number must be 10 digits.")
            return render(request,'manager/manager_signup.html')

        if len(password) < 6:
            messages.error(request, "Password must be 6 digit")
            return render(request,'manager/manager_signup.html')



        if password != confirm_password:
            messages.error(request, "Password and Confirm Password must be Same")
            return render(request,'manager/manager_signup.html')

        manager_user = LoginSide.objects.create_user(username=manager_username,
                                                     first_name=first_name,
                                                     last_name=last_name,
                                                     photo=profile_img,
                                                     password=password,
                                                     email=manager_email,
                                                     phone_number=phone,
                                                     login_role="Handler")
        manager_user.save()

        return redirect('Admin_Dashboard')
    return render(request,'manager/manager_signup.html')

@login_required(login_url='manager-login')
def manager_logout(request):
    logout(request)
    return redirect('manager-login')




def about_yi(request):
    return render(request,'components/AboutYi.html')

@login_required(login_url='manager-login')
def manager_update(request,manager_id):
    if request.user.login_role == "Handler":
        if request.method == 'POST':
            manager_profile = get_object_or_404(LoginSide, id=manager_id)
            manager_profile.first_name = request.POST['manager_first_name']
            manager_profile.last_name = request.POST['manager_last_name']
            manager_profile.email = request.POST['manager_email']
            manager_profile.username = request.POST['username']
            manager_profile.phone_number = request.POST['phone_number']
            if 'manager_profile_img' in request.FILES:
                manager_profile.photo = request.FILES['manager_profile_img']
            manager_profile.save()
        return redirect('manager-profile')
    return render(request,'manager/manager_profile.html')

@login_required(login_url='manager-login')
def manager_password(request):
    if request.user.login_role == "Handler":
        if request.method == 'POST':
            old_password = request.POST.get('old_password')
            new_password = request.POST.get('new_password')
            confirm_password = request.POST.get('confirm_password')
            manager_user =request.user

            if not manager_user.check_password(old_password):
                messages.error(request,"Old Password Incorrect")
                return redirect('manager-profile')

            if len(new_password)  < 6 :
                messages.error(request, "Password must be 6 digit")
                return redirect('manager-profile')

            if new_password != confirm_password:
                messages.error(request,"New Password and Confirm Password must Be same" )
                return redirect('manager-profile')
            manager_user.set_password(new_password)
            manager_user.save()
            update_session_auth_hash(request,manager_user)
            return redirect('manager-profile')

@login_required(login_url='manager-login')
def manager_dashboard(request):
    if request.user.login_role != 'Handler':
        return redirect('Error-Page')
    return render(request,'manager/manager_dashboard.html')

@login_required(login_url='manager-login')
def manager_profile(request):
    if request.user.login_role != 'Handler':
        return redirect('Error-Page')

    return render(request,'manager/manager_profile.html')

@login_required(login_url='manager-login')
def event_list(request):
    # Ensure the user has the 'Handler' role
    if request.user.login_role != 'Handler':
        return redirect('manager-profile')
    user = request.user
    all_event = Event_Data.objects.filter(user=user)
    context = {
        'user': user,
        'k1': all_event
    }
    return render(request, 'manager/event_list.html', context)



def delete_event_handler(request,events_id):
    if request.user.login_role != 'Handler':
        return redirect('Error-Page')
    if request.method == 'POST':
        delete_events = get_object_or_404(Event_Data,id=events_id)
        delete_events.delete()

    return redirect('event-list')



def update_event(request,event_id):
    if request.user.login_role != 'Handler':
        return redirect('Error-Page')
    update_event_data = get_object_or_404(Event_Data,id=event_id)
    if request.method == 'POST':
        update_event_data.your_name = request.POST['your_name']
        update_event_data.date = request.POST['date']
        update_event_data.role_yi = request.POST['role_yi']
        update_event_data.project_vertical = request.POST['project_vertical']
        update_event_data.project_stakeholder = request.POST['project_stakeholder']
        update_event_data.yi_pillar = request.POST['yi_pillar']
        update_event_data.social_link = request.POST['social_link ']
        update_event_data.which_SIG = request.POST['which_SIG']
        update_event_data.event_handle = request.POST['event_handl']
        update_event_data.total_impact= request.POST['total_impact']
        update_event_data.save()
    return redirect('event-list')



@login_required(login_url='manager-login')
def event_data(request):
    if request.user.login_role == 'Handler':
        if request.method == 'POST':
            your_name = request.POST['your_name']
            event_date = request.POST['event_date']
            role_yi = request.POST['role_yi']
            sig_option = request.POST.get('sig_')
            event_handle = request.POST['event_handle']
            project_verticals = request.POST['project_verticals']
            project_stakeholder = request.POST['project_stakeholder']
            yi_pillar = request.POST['yi_pillar']
            social_link = request.POST['social_link']
            total_impact = request.POST['total_impact']
            Event_Data.objects.create(your_name=your_name,date=event_date,role_yi=role_yi,event_handle=event_handle,project_vertical=project_verticals,which_SIG=sig_option,
                                      project_stakeholder=project_stakeholder,yi_pillar=yi_pillar,social_link=social_link,total_impact=total_impact,user=request.user)
            return  redirect('event-list')

from django.db.models import Avg, Sum

def chart(request):
    if request.user.login_role != 'Handler':
        return redirect('Error-Page')
    user = request.user
    # user_data  = Event_Data.objects.filter(user=user)

    total_event = Event_Data.objects.filter(user=user).count()


    total_impact_data =  Event_Data.objects.filter(user=user).aggregate(Sum('total_impact'))
    total_impact = total_impact_data['total_impact__sum'] if total_impact_data['total_impact__sum']is not None else 0

    context = {  'total_event':total_event,
               'total_impact':total_impact   }

    return render(request,'chart/chart.html',context)


matplotlib.use('Agg')

def pie_chart(request):


    user = request.user
    user_data = Event_Data.objects.filter(user=user)
    


    impact = np.array([i.total_impact for i in user_data])
    date = [i.project_vertical for i in user_data]


    plt.figure(figsize=(8,5))
    plt.pie(impact,labels=date,autopct='%1.1f%%',)
    plt.title("Project Verticals  ",fontsize=12,fontname='Cambria')


    buffer =BytesIO()
    plt.savefig(buffer,format='jpg')
    buffer.seek(0)


    plt.close()

    return HttpResponse(buffer,content_type='image/jpg')



def stackholder_chart(request):
    user = request.user
    user_data = Event_Data.objects.filter(user=user)

    impact = np.array([i.total_impact for i in user_data])
    stake_holder = [i.project_stakeholder for i in user_data]

    plt.figure(figsize=(8,5))
    plt.pie(impact,labels=stake_holder,autopct='%1.1f%%')
    plt.title("Stackeholder wise Impact",fontsize=12,fontname='Cambria')


    buffer = BytesIO()
    plt.savefig(buffer,format='jpg')
    buffer.seek(0)

    plt.close()

    return HttpResponse(buffer,content_type='image/jpg') 



def project_chart(request):
    user = request.user
    user_data = Event_Data.objects.filter(user=user)
    x = [i.project_vertical for i in user_data]
    y = [i.total_impact for i in user_data]


    total_impact = sum(y)
    plt.figure(figsize=(20,5))


    bar = plt.bar(x,y)
    plt.bar_label(bar, labels=[f'{value}' for value in y])
    plt.title("Project Wise Impact",fontname='Cambria',fontsize=20)
    plt.xlabel("Project Verticals",fontname='Cambria',)
    plt.ylabel("Impact",fontname='Cambria')

    

    buffer = BytesIO()
    plt.savefig(buffer,format='jpg')
    buffer.seek(0)

    plt.close()
    return HttpResponse(buffer,content_type='image/jpg')


