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
from django.db.models import Avg, Sum

# Create your views here.


def manager_login(request):
    if request.method == 'POST':
        username = request.POST.get('manager_username')
        password = request.POST.get('manager_password')

        manager_user = authenticate(request,username=username,password=password)
        if manager_user is not None:
            if manager_user.login_role.filter(name='Manager').exists():
                login(request,manager_user)
                return redirect('manager-dashboard')
            else:
                messages.error(request,"Incorrect Username Password")
        else:
            messages.error(request, "Invalid Username or Password")
            return redirect('index')


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
        # which_role = request.POST.getlist('which_role')





        if len(phone) != 10 or not phone.isdigit():
            messages.error(request, "Phone number must be 10 digits.")
            return render(request,'manager/manager_signup.html')

        if len(password) < 8 or not any(c.isupper() for c in password) or not any(
                c in "!@#$%^&*()_+-={}[]|\\:;\"'<>,.?/~`" for c in password):
            messages.error(request,"Password must be at least 8 characters with one uppercase letter and one special character")
            return render(request, 'manager/manager_signup.html')

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
                                                     login_role='Manager',)
        manager_user.save()
        messages.success(request, 'New Manager Created')
        return redirect('manager-signup')
    return render(request,'manager/manager_signup.html')



@login_required(login_url='manager-login')
def manager_logout(request):
    logout(request)
    return redirect('index')




def about_yi(request):
    return render(request,'components/AboutYi.html')

@login_required(login_url='manager-login')
def manager_update(request,manager_id):
    if request.user.login_role.filter(name='Manager').exists():
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
            messages.success(request,'Profile Updated')
            return redirect('manager-profile')
        else:
            messages.error(request,'Profile Not updated')
            return redirect('manager-profile')
    return render(request,'manager/manager_profile.html')

@login_required(login_url='manager-login')
def manager_password(request):
    if request.user.login_role.filter(name='Manager').exists():
        if request.method == 'POST':
            old_password = request.POST.get('old_password')
            new_password = request.POST.get('new_password')
            confirm_password = request.POST.get('confirm_password')
            manager_user =request.user

            if not manager_user.check_password(old_password):
                messages.error(request,"Old Password Incorrect")
                return redirect('manager-profile')

            if len(new_password) < 8 or not any(c.isupper() for c in new_password) or not any(
                    c in "!@#$%^&*()_+-={}[]|\\:;\"'<>,.?/~`" for c in new_password):
                messages.error(request,
                               "Password must be at least 8 characters with one uppercase letter and one special character")
                return redirect('manager-profile')

            if new_password != confirm_password:
                messages.error(request,"New Password and Confirm Password must Be same" )
                return redirect('manager-profile')
            manager_user.set_password(new_password)
            manager_user.save()
            messages.success(request,'Password Updated')
            update_session_auth_hash(request,manager_user)
            return redirect('manager-profile')
        else:
            messages.error(request,'Manager not Created')
            return redirect('manager-profile')

@login_required(login_url='manager-login')
def manager_dashboard(request):
    if not request.user.login_role.filter(name='Manager').exists():
        return redirect('Error-Page')
    return render(request,'manager/manager_dashboard.html')

@login_required(login_url='manager-login')
def manager_profile(request):
    if not request.user.login_role.filter(name='Manager').exists():
        return redirect('Error-Page')

    return render(request,'manager/manager_profile.html')

@login_required(login_url='manager-login')
def event_list(request):
    # Ensure the user has the 'Manager' role
    if not request.user.login_role.filter(name='Manager').exists():
        return redirect('manager-profile')
    user = request.user
    all_event = Event_Data.objects.filter(user=user)
    context = {
        'user': user,
        'k1': all_event
    }
    return render(request, 'manager/event_list.html', context)



def delete_event_user(request,events_id):
    if not request.user.login_role.filter(name='Manager').exists():
        return redirect('Error-Page')
    if request.method == 'POST':
        delete_events = get_object_or_404(Event_Data,id=events_id)
        delete_events.delete()
    return redirect('event-list')


def update_event_data(request,update_id):
    if not request.user.login_role.filter(name='Manager').exists():
        return redirect('Error-page')
    else:
        if request.user.login_role.filter(name='Manager').exists():
            update_event = get_object_or_404(Event_Data,id = update_id)
            update_event.collage =  request.POST['collage']
            update_event.school = request.POST['school']
            update_event.date = request.POST['event_date']
            update_event.role_yi = request.POST['role_yi']
            update_event.project_vertical = request.POST['project_verticals']
            update_event.project_stakeholder = request.POST['project_stakeholder']
            update_event.yi_pillar = request.POST['yi_pillar']
            update_event.social_link = request.POST['social_link']
            update_event.event_handle = request.POST['event_handle']
            update_event.total_impact = request.POST['total_impact']
            update_event.which_SIG  = request.POST['sig_']

            update_event.associate_partner = request.POST.get('associate_partners')
            update_event.save()
            messages.success(request,'Data update')
            return redirect('event-list')
        else:
            messages.error(request,'Data not update')







# def update_event(request,event_id):
#     if request.user.login_role != 'Manager':
#         return redirect('Error-Page')
#     update_event_data = get_object_or_404(Event_Data,id=event_id)
#     if request.method == 'POST':
#         update_event_data.your_name = request.POST['your_name']
#         update_event_data.date = request.POST['date']
#         update_event_data.role_yi = request.POST['role_yi']
#         update_event_data.project_vertical = request.POST['project_verticals']
#         update_event_data.project_stakeholder = request.POST['project_stakeholder']
#         update_event_data.yi_pillar = request.POST['yi_pillar']
#         update_event_data.social_link = request.POST['social_link ']
#         update_event_data.which_SIG = request.POST['which_SIG']
#         update_event_data.event_handle = request.POST['event_handl']
#         update_event_data.total_impact= request.POST['total_impact']
#         update_event_data.save()
#     return redirect('event-list')
# def delete_event(request):


# def manager_list(request):
#     if not request.user.login_role.filter(name='Admin').exists():
#         return redirect('Error-Page')
#     admin_role = Login_Role.objects.get(name='Admin')
#     managers = LoginSide.objects.filter(login_role=admin_role)
#     contex = {
#         'managers' :managers
#     }
#     return render(request,'Admin/view_manager.html',contex)


@login_required(login_url='manager-login')
def event_data(request):
    if request.user.login_role.filter(name='Manager').exists():
        if request.method == 'POST':
            your_name = request.POST['your_name']
            event_date = request.POST['event_date']
            role_yi = request.POST['role_yi']
            sig_option = request.POST.get('sig_','')
            event_handle = request.POST['handel_by']
            project_verticals = request.POST['project_verticals']
            project_stakeholder = request.POST['project_stakeholder']
            yi_pillar = request.POST['yi_pillar']
            social_link = request.POST['social_link']
            total_impact = request.POST['total_impact']
            event_expense = request.POST['event_expense']
            event_venue = request.POST['event_venue']
            event_name = request.POST['event_name']
            event_images =  request.FILES.get('event_img')
            school = request.POST['school']
            collage = request.POST['collage']
            associate_partner = request.POST.get('associate_partner','')

            if event_images.size > 1 * 1024 * 1024:
                messages.error(request, 'Each image must be 4MB or less')
                return redirect('event_data')

            Event_Data.objects.create(
                your_name=your_name,
                date=event_date,
                role_yi=role_yi,
                event_handle=event_handle,
                project_vertical=project_verticals,
                which_SIG=sig_option,
                project_stakeholder=project_stakeholder,
                yi_pillar=yi_pillar,
                social_link=social_link,
                event_venue=event_venue,
                event_expense=event_expense,
                school=school,
                collage=collage,
                total_impact=total_impact,
                event_name=event_name,
                event_photo=event_images,
                associate_partner=associate_partner,
                user=request.user
            )

            messages.success(request, 'thank you for insert data')
        return redirect('event-list')





def chart(request):
    if not request.user.login_role.filter(name='Manager').exists():
        return redirect('Error-Page')
    user = request.user
    all_event = Event_Data.objects.filter(user=user)
    total_event = Event_Data.objects.filter(user=user).count()
    total_impact_data =  Event_Data.objects.filter(user=user).aggregate(Sum('total_impact'))
    total_impact = total_impact_data['total_impact__sum'] if total_impact_data['total_impact__sum']is not None else 0
    event_name = Event_Data.objects.filter(user=user).values_list('project_vertical',flat=True).distinct()
    # event_impact = Event_Data.objects.filter(user=user).values('project_vertical').annotate(total_impact=Sum('total_impact'))
    event_impact = Event_Data.objects.filter(user=user).values('project_vertical').annotate(total_impact=Sum('total_impact'))
    # Map event names to their corresponding total impact
    event_impact_dict = {item['project_vertical']: item['total_impact'] for item in event_impact}

    # Adjust event_impact to reflect the correct order of event_name
    aligned_event_impact = [event_impact_dict.get(event, 0) for event in event_name]

    # print(event_name)
    # print(event_impact)

    context = {  'total_event':total_event,
               'total_impact':total_impact,
                 'event_name': event_name,
                 'impact':aligned_event_impact,
                 }

    return render(request,'chart/chart.html',context)




# Masoom Side

def masoom_dashboard(request):
    return render(request,'Masoom/masoom_dashboard.html')