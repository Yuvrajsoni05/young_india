

from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import login,authenticate,logout,update_session_auth_hash
from admin_app.models import LoginSide
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
            return redirect('manager-login')
    return render(request,'manager/manager_login.html')
@login_required(login_url='Admin_Login')
def manager_signup(request):
    if request.method == "POST":
        manager_username = request.POST.get('manager_username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        password = request.POST.get('password1')
        profile_img = request.FILES.get('profile_img')
        confirm_password = request.POST.get('password2')
        manager_email = request.POST.get('manager_email')
        if password != confirm_password:
            return render(request,'manager/manager_login.html')

        manager_user = LoginSide.objects.create_user(username=manager_username,
                                                     first_name=first_name,
                                                     last_name=last_name,
                                                     photo=profile_img,
                                                     password=password,
                                                     email=manager_email,
                                                     login_role="Handler")
        manager_user.save()
        login(request,manager_user)
        return redirect('Admin_Dashboard')
    return render(request,'manager/manager_signup.html')

@login_required(login_url='manager-login')
def manager_logout(request):
    logout(request)
    return redirect('manager-login')

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
                return redirect('manager_dashboard')
            if new_password != confirm_password:
                return redirect('manager_dashboard')
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
    all_event = Event_Data.objects.filter(user=user)  # Filter the events for the logged-in user

    context = {
        'user': user,
        'k1': all_event
    }

    return render(request, 'manager/event_list.html', context)


@login_required(login_url='manager-login')
def event_data(request):
    if request.user.login_role == 'Handler':
        if request.method == 'POST':
            your_name = request.POST['your_name']
            event_date = request.POST['event_date']
            role_yi = request.POST['role_yi']
            sig_option = request.POST['sig_select']
            event_handle = request.POST['event_handle']
            project_verticals = request.POST['project_verticals']
            project_stakeholder = request.POST['project_stakeholder']
            yi_pillar = request.POST['yi_pillar']
            social_link = request.POST['social_link']
            total_impact = request.POST['total_impact']
            Event_Data.objects.create(your_name=your_name,date=event_date,role_yi=role_yi,event_handle=event_handle,project_vertical=project_verticals, which_SIG=sig_option,
                                      project_stakeholder=project_stakeholder,yi_pillar=yi_pillar,social_link=social_link,total_impact=total_impact,user=request.user)
            return  redirect('event-list')




