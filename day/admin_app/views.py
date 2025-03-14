from collections import Counter
from io import BytesIO
import re
# from openpyxl.drawing.image import Image
from django.core.paginator import Paginator
# import matplotlib
import numpy as np
from PIL.Image import Image
from asgiref.typing import HTTPResponseBodyEvent
from django.db.models import Avg, Sum
from django.shortcuts import render,redirect,get_object_or_404
from matplotlib import pyplot as plt
from rest_framework.reverse import reverse_lazy
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import *
from django.contrib.auth import login, authenticate, update_session_auth_hash ,logout
from django.contrib.auth.decorators import login_required
# import logging
from django.http import HttpResponse
import openpyxl
from django.core.validators import FileExtensionValidator 
from manager_app.models import Event_Data,Event_Image
from django.contrib import messages

from django.shortcuts import render
from django.views.decorators.cache import never_cache
import openpyxl
from openpyxl import Workbook
from openpyxl.styles import Alignment
from openpyxl.drawing.image import Image
# from io import BytesIO
# from PIL import Image as PILImage
from django.http import HttpResponse
import os
from django.conf import settings
from openpyxl.styles import Alignment, Font
from django.contrib.sessions.models import Session
from django.utils.timezone import now
from django.contrib.auth.models import User

#Json Response
from django.http import JsonResponse


# DRF API
from .serializer import EventDataSerializer
from django.utils.decorators import method_decorator
from rest_framework import status



# Password Side
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView
from django.urls import reverse_lazy
# Create your views here.










# login Page 

def index(request):
    try:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

           
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)  # Log the user in

         
                if user.login_role.filter(name='Admin').exists():
                    # print(f"{username} , {password}")
                   # logger.info(f"Someone is trying to login Name : {username} {password}")
                    return redirect('Admin_Dashboard')
                else:
                    
                    roles = user.login_role.all() 
                    request.session['userrole'] = [role.name for role in roles]  # Get all roles associated with the user
                    return redirect('manager-dashboard')
            else:
              
                messages.error(request, "Invalid credentials, please try again.")
                # logger.info(f"Error during authentication: {str(e)}")
                return redirect('index')
    except Exception as e:

        messages.error(request, f"Error")
        # Optionally, log the exception for debugging purposes (e.g., using Python's logging module)
        # 
        # logger = logging.getLogger(__name__)
        # logger.error(f"Someone is trying to login Name : {username} {password}")
        # return render(request, 'index.html')

    # If it's a GET request, render the login page
    return render(request, 'index.html')

    


  
   
    # if request.method == 'POST':
    #     username = request.POST.get('username')
    #     password = request.POST.get('password')
    #     #login_roles = request.POST.get('login_roles')  # Selected role from form input

    #     # Authenticate the user
    #     user = authenticate(request, username=username, password=password)

    #     if user is not None:
    #         if user.login_role.filter(name='Admin').exists():
    #             login(request,user)
    #             return redirect('Admin_Dashboard')
            
    #         else:
    #             return redirect('manager-dashboard')


        # if user is not None:
            
        #     # Ensure user is a LoginSide instance (if using a custom user model)
        #     if isinstance(user, LoginSide):
        #         if user.login_role.name == 'Admin':
        #             return redirect('Admin_Dashbaord')
                
        #         # Get the selected role from the database

               
        #         selected_role = Login_Role.objects.filter(name=login_roles).first()

        #         if selected_role and selected_role in user.login_role.all():  # Check if user has the selected role
        #             login(request, user)

        #             # Store the role in the session so that it can be accessed across requests
        #             request.session['user_roles'] = selected_role.name

        #             # Redirect based on role
        #             if selected_role.name == 'Admin':  # If user has Admin role
        #                 return redirect('Admin_Dashboard')
        #             else:
        #                 return redirect('manager-dashboard')
        #         else:
        #             # Role doesn't match, redirect back to the login page
        #             messages.error(request, "Role not match")
        #             return redirect('index')
        #     else:
        #         # In case of an invalid user instance
        #         messages.error(request, "username is Invalid")
        #         return redirect('index')
        # else:
        #     # If authentication fails, redirect to login page
        #     messages.error(request, "Login Again PlZ")
        #     return redirect('index')

    # # Get all roles to pass to the form
    # roles = Login_Role.objects.all()
    # context = {
    #     'roles': roles
    # }
    # return render(request, 'index.html', context)







# def Admin_Login(request):
#     if request.method == 'POST':
#         username = request.POST.get('admin_username')
#         password = request.POST.get('admin_password')

#         # Authenticate the user
#         Admin_user = authenticate(request, username=username, password=password)

#         if Admin_user is not None:
#             # Check if the authenticated user has the 'Admin' role
#             if Admin_user.login_role.filter(name='Admin').exists():  # Assuming 'Admin' is the role name
#                 # Log the user in
#                 login(request, Admin_user)
#                 return redirect('Admin_Dashboard')
#             else:
#                 messages.error(request, "You do not have permission to access the admin panel.")
#                 return redirect('index')  # Redirect to the homepage or another page if not an Admin
#         else:
#             messages.error(request, "Invalid Username or Password")
#             return redirect('index')  # Redirect back to the login page if credentials are incorrect

#     return render(request, 'index.html')






def get_username(request):
    user  = request.user
    data = {
        "username": "Yuvraj Soni" # You can customize this with any name
    }
    return JsonResponse(data)


#    try:
#                     validator = FileExtensionValidator(allowed_extensions=['jpeg', 'jpg', 'png'])
#                     validator(profile_img)  # Validate the image extension
#                 except ValidationError:
#                     messages.error(request, "Invalid file type. Only .jpeg, .jpg, .png allowed.")
#                     return redirect('Admin_Signup')

# Add new User Ec members
@login_required(login_url='index')
def Admin_Signup(request):
        if not request.user.login_role.filter(name='Admin').exists():
            return redirect('Error-Page')
        
        sessions = Session.objects.filter(expire_date__gte=now())
    # Get user ids from the session data
        user_ids = [session.get_decoded().get('_auth_user_id') for session in sessions]
        # Query LoginSide objects for users
        active_users = LoginSide.objects.filter(id__in=user_ids)  # Get user objects
        
        active_user_names = [f"{user.first_name} {user.last_name}" for user in active_users]  
        active_users_count = LoginSide.objects.filter(is_active=True).count()
        
        active_users_count = active_users.count()

        try:
            
            
            if request.method == 'POST':
                            
                username = request.POST.get('add_username')
                first_name = request.POST.get('first_name')
                last_name = request.POST.get('last_name')
                password = request.POST.get('password1')
                profile_img = request.FILES.get('profile_img')
                confirm_password = request.POST.get('password2')
                Admin_email = request.POST.get('add_email')
                phone = request.POST.get('add_phone')
                yi_role = request.POST.get('yi_role')
                login_role = request.POST.getlist('login_role')  # Use getlist to fetch multiple roles

                
                fields = [username, first_name, last_name, password, confirm_password, Admin_email, phone, yi_role, login_role]
                if any(field is  None  for field in fields ):
                    messages.error(request,"All Filed Are Required")
                    return redirect('Admin_Signup') 

            
                if profile_img is not  None:
                    
                    
                    try:
                        
                        validator = FileExtensionValidator(allowed_extensions=['jpeg', 'jpg', 'png'])
                        validator(profile_img)  
                    except ValidationError:
                        messages.error(request, "Invalid file type. Only .jpeg, .jpg, .png allowed.")
                        return redirect('Admin_Signup')
                        
                    
                    if profile_img.size > 4*1024*1024  :
                        
                        messages.error(request,'Image Size must be 4mb')
                        return redirect('Admin_Signup')
                
                    
    
                # valid_extensions = ['.jpeg','.jpg','.png']

                # for img in profile_img:
                #     ext = os.path.splitext(img.name)[1]
                #     if ext.lower() not in valid_extensions:
                #         messages.error(request,f"Invalid File . only .jpeg .png .jpeg")
                #         return redirect('Admin_Signup')

                if LoginSide.objects.filter(email=Admin_email).exists():
                    messages.error(request, "This email is already taken.")
                    return redirect('Admin_Signup')

                if LoginSide.objects.filter(username=username).exists():
                    messages.error(request, "This Username is already taken.")
                    return redirect('Admin_Signup')
                
                
                regex = r'^(\+91[\-\s]?)?[0]?(91)?[789]\d{9}$'
                
                if not re.match(regex,phone):
                    messages.error(request, "Phone number must be 10 digits. and valid phone number")
                    return redirect('Admin_Signup')
                    

                # if len(phone) != 10 or not phone.isdigit() or regex:
                #     messages.error(request, "Phone number must be 10 digits. and valid phone number")
                #     return redirect('Admin_Signup')
        
                    

                if len(password) < 8 or not any(c.isupper() for c in password) or not any(
                        c in "!@#$%^&*()_+-={}[]\\:;\"'<>,.?/~`" for c in password):
                    messages.error(request,
                                "Password must be at least 8 characters with one uppercase letter and one special character")
                    return redirect('Admin_Signup')

                if password != confirm_password:
                    messages.error(request, "Password and confirm Password must be same ")
                    return redirect('Admin_Signup')

                # Create user
                Admin_User = LoginSide.objects.create_user(
                        username=username,
                        first_name=first_name,
                        last_name=last_name,
                        photo=profile_img,
                        password=password,
                        email=Admin_email,
                        yi_role=yi_role,
                        phone_number=phone
                    )

                    # Assign selected roles to the user
                roles = Login_Role.objects.filter(name__in=login_role)  # Filter roles based on selected ones
                Admin_User.login_role.set(roles)  # Assign multiple roles
                    
                

            
                        
                Admin_User.full_clean()
                Admin_User.save()
                messages.success(request, "New Executive Council Member Add")
                return redirect('Admin_Dashboard')

                

            # Fetch all roles for the dropdown
            login_role = Login_Role.objects.all()
            context = {
                'role': login_role,
                'name':active_user_names,
                'count':active_users_count
            }
            
            return render(request, 'Admin/AdminSignup.html', context)
    
        except Exception as e :
            messages.error(request,f'New User not Add Something went Worng Plz Try again ' )
            return render(request, 'Admin/AdminSignup.html')
    
    



# Admin Profie  HTML Page

@login_required(login_url='index')
def Admin_Profile(request):
    if not request.user.login_role.filter(name='Admin').exists():
        return redirect('Error-Page')
    
    
    sessions = Session.objects.filter(expire_date__gte=now())
    # Get user ids from the session data
    user_ids = [session.get_decoded().get('_auth_user_id') for session in sessions]
    # Query LoginSide objects for users
    active_users = LoginSide.objects.filter(id__in=user_ids)  # Get user objects
    
    active_user_names = [f"{user.first_name} {user.last_name}" for user in active_users]  
    active_users_count = LoginSide.objects.filter(is_active=True).count()
  
    active_users_count = active_users.count()
    context = {
            'name':active_user_names,
            'count':active_users_count,
    }
    # else:
    #     return redirect('Admin_Profile',)
    return render(request, 'Admin/Admin_Profile.html',context)


#Admin profile Update View Code 

@login_required(login_url='index')
def Admin_update(request, admin_id):
    # Check if the user has 'Admin' role
    if not request.user.login_role.filter(name='Admin').exists():
        messages.error(request, 'You do not have permission to access this page.')
        return redirect('Error-Page')
    
    try:
        # Ensure method is POST to update profile
        if request.method == 'POST':
            admin_profile = get_object_or_404(LoginSide, id=admin_id)

            # Update fields from POST data
            admin_profile.first_name = request.POST.get('admin_firstname', admin_profile.first_name)
            admin_profile.last_name = request.POST.get('admin_lastname', admin_profile.last_name)
            admin_profile.email = request.POST.get('admin_email', admin_profile.email)
            admin_profile.username = request.POST.get('admin_username', admin_profile.username)
            admin_profile.phone_number = request.POST.get('admin_phone', admin_profile.phone_number)

          
            if 'admin_profile_img' in request.FILES:
                admin_profile.photo = request.FILES['admin_profile_img']
                if admin_profile.photo.size > 4*1024*1024:
                    messages.error(request,'Image Size must be 4mb')
                    return redirect('Admin_Profile')
            try:
                admin_profile.full_clean()
                admin_profile.save()
                messages.success(request,'Profile successfully updated.')
                return redirect('Admin_Profile')
            except Exception as e:
                for field,errors in e.message_dict.items():
                    for error in errors:
                        messages.error(request,f"{error} ")
                    return redirect('Admin_Profile')
        # If the method is not POST, show an error
        else:
            messages.error(request, 'Invalid request method. Profile not updated.')
            return redirect('Admin_Profile')

    except Exception as e:
        # Handle any other errors during the process
        messages.error(request, f'Error updating profile: {str(e)}')
        return redirect('Admin_Profile')

#Admin password  Update

@login_required(login_url='index')
def admin_password(request):
    if request.user.login_role.filter(name='Admin').exists():
        try:


            if request.method == 'POST':
                old_password = request.POST.get('old_password')
                new_password = request.POST.get('new_password')
                confirm_password = request.POST.get('confirm_password')
                admin_user =request.user
                if not admin_user.check_password(old_password):
                    messages.error(request, "Old Password Incorrect")
                    return redirect('Admin_Profile')

                if len(new_password) < 8 or not any(c.isupper() for c in   new_password) or not any(
                        c in "!@#$%^&*()_+-={}[]\\:;\"'<>,.?/~`" for c in new_password):
                    messages.error(request,  "Password must be at least 8 characters with one uppercase letter and one special character")
                    return redirect('Admin_Profile')

                if new_password != confirm_password:
                    messages.error(request, "New Password and Confirm Password must Be same")
                    return redirect('Admin_Profile')

                admin_user.set_password(new_password)
                admin_user.save()
                messages.success(request,'Password Updated ')
                update_session_auth_hash(request,admin_user)
                return redirect('Admin_Profile')
            else:
                return redirect('Error-Page')
        except Exception as e:
            messages.error(request,'Somthing Wrong ',str(e))


# Admin Logout

@login_required(login_url='index')
def admin_logout(request):
    logout(request)
    request.session.clear()
    return redirect('index')



# Admin Dashboard 

@login_required(login_url='index')
def Admin_Dashboard(request):
    
    if not request.user.login_role.filter(name='Admin').exists():
        return redirect('Error-Page')
    
    # You don't need to reassign user_id since it's already passed in the URL
   
    total_event = Event_Data.objects.count()
    user_id = request.user.id
   
    total_user_data = LoginSide.objects.exclude(login_role='Admin')

    total_user = total_user_data.count()
    

    sessions = Session.objects.filter(expire_date__gte=now())
    # Get user ids from the session data
    user_ids = [session.get_decoded().get('_auth_user_id') for session in sessions]
    # Query LoginSide objects for users
    active_users = LoginSide.objects.filter(id__in=user_ids)  # Get user objects
    
    active_user_names = [f"{user.first_name} {user.last_name}" for user in active_users]  
    active_users_count = LoginSide.objects.filter(is_active=True).count()
  
    active_users_count = active_users.count()
    
    total_expense_result = Event_Data.objects.aggregate(Sum('event_expense'))
    total_expense = total_expense_result['event_expense__sum'] if total_expense_result['event_expense__sum'] is not None else 0
    total_impact_result = Event_Data.objects.aggregate(Sum('total_impact'))
    total_impact = total_impact_result['total_impact__sum'] if total_impact_result['total_impact__sum'] is not None else 0
    # def format_total_impact(total_impact):
    #     try:
    #         # Convert total_impact to a float
    #         value = float(total_impact)
            
    #         # Format as K if the value is 1000 or greater
    #         if value >= 100000 :
    #             return f"{value / 1000:.0f}L"
         
            
    #         # Return the value as string if it's less than 1000
    #         return str(value)
        
    #     except Exception as e:
    #         # Log the error for debugging (can replace with proper logging in production)
    #         print(f"Error formatting total impact: {e}")
    #         return str(total_impact)  # Return the raw value if there's an error

# Apply the function to your total_impact
    # formatted_total_impact = format_total_impact(total_impact)

    # Calculate average impact
    impact_avg = Event_Data.objects.aggregate(Avg('total_impact'))
    avg_impact = impact_avg['total_impact__avg'] if impact_avg['total_impact__avg'] is not None else 0

    # Retrieve all distinct users and roles
    all_user = LoginSide.objects.all().distinct()
    login_role = Login_Role.objects.all().distinct()

    # Manager names from Event_Data
    manager_name = Event_Data.objects.all().values_list('your_name', flat=True).distinct()
    
    # Handle search filtering
    search = request.GET.get('search')
    if search and search != 'all':
        event_list = Event_Data.objects.filter(your_name__icontains=search)  # Using icontains for partial match
    else:
        event_list = Event_Data.objects.all()

    context = {
        'user_id':user_id,
        'users_data': all_user,
        'role': login_role,
        'total_manager': total_user,
        'total_event': total_event,
        'total_impact': total_impact ,
        'impact_avg': avg_impact,
        'total_expense': total_expense,
        'events': event_list,
        'm1': manager_name,
        'count':active_users_count,
        'name':active_user_names
    }

    return render(request, 'Admin/AdminDashboard.html', context)


# Base file 
@login_required(login_url='index')
def base(request):
    sessions = Session.objects.filter(expire_date__gte=now())
    # Get user ids from the session data
    user_ids = [session.get_decoded().get('_auth_user_id') for session in sessions]
    # Query LoginSide objects for users
    active_users = LoginSide.objects.filter(id__in=user_ids)  # Get user objects
    
    active_user_names = [f"{user.first_name} {user.last_name}" for user in active_users]  
    active_users_count = LoginSide.objects.filter(is_active=True).count()
  
    active_users_count = active_users.count()
    
    context = {
        'count':active_users_count,
        'name':active_user_names
    }
    
    return render(request,'base/base.html',context)


# def getuser(request):
#     query = LoginSide.objects.all()
#     return JsonResponse({"user":list(query.values)})
# def active_users_count(request):
   
#     return render(request, 'dashboard.html', {'active_users_count': active_users.count()})


# def Login_data(request):
#     role = request.GET.get('search')
#     login_data = Login_Role.objects.all().values_list('name', flat=True).distinct()

#     # Handle the case when 'role' is 'alls' or not provided
#     if role == 'alls' or role is None:
#         role_list = Login_Role.objects.all()  # Fetch all roles
#     else:
#         role_list = Event_Data.objects.all()  # Or modify this logic if you need a different filter

#     context = {
#         'd1': login_data,  # Renamed 'd1' to a more descriptive name
#         'role_list': role_list,
#     }

#     return render(request, 'Admin/AdminDashboard.html', context)
# def Role_List(request):
    
#     role_data = Login_Role.objects.all().values_list('name',flat=True).distinct()
#     role = request.GET.get('role_serach')

#     if role and role != 'all':
#         role_list = Event_Data.objects.filter(login_role = role)
#     else:
#         role_list = Event_Data.objects.all()

#     context = {

#         'role_datas' : role_list,
#     }
#     return render(request,'Admin/AdminDashboard.html',context)



# Admin Side Event Data 

@login_required(login_url='index')
def admin_event_data(request):
    try:
        if not request.user.login_role.filter(name='Admin'):
            return redirect('Error-Page')
    except Exception:
        return redirect('Error-Page')
    
    
    
    sessions = Session.objects.filter(expire_date__gte=now())
    # Get user ids from the session data
    user_ids = [session.get_decoded().get('_auth_user_id') for session in sessions]
    # Query LoginSide objects for users
    active_users = LoginSide.objects.filter(id__in=user_ids)  # Get user objects
    
    active_user_names = [f"{user.first_name} {user.last_name}" for user in active_users]  
    active_users_count = LoginSide.objects.filter(is_active=True).count()
  
    active_users_count = active_users.count()
    
    
    
    try:
         
        
        if request.method  == 'POST':
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
        
            school = request.POST['school']
            collage = request.POST['collage']
            associate_partner = request.POST.get('associate_partner','')


            event_image = request.FILES.getlist('event_img')

            if len(event_image)>6 and event_image:
                messages.error(request,"You can Upload only 6 Image")
                return redirect('admin_event_data')
            
            valid_extension = ['.jpeg','.jpg','.png']


            for img in event_image:
                ext =  os.path.splitext(img.name)[1]
                if ext.lower() not in valid_extension:
                    messages.error(request,f"Invalid file type: {img.name} . Only .jpg, .jpeg, and .png are allowed.")
                    return redirect('admin_event_data')

            event_data = Event_Data.objects.create(
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
            
                associate_partner=associate_partner,
                user=request.user
            )
            for image in event_image:
                Event_Image.objects.create(event_photo=image,event=event_data)

            messages.success(request,'Thank you Insert Data  ')
            return redirect('Admin_Dashboard')
        context = {
        'count':active_users_count,
        'name':active_user_names
    }

        return render(request,'Admin/Admin_Event_data.html',context)
    except Exception:
        messages.error(request,"Somthing Went  Please  Try Again")
        return redirect('Admin_Dashboard')


# List of  Events

@login_required(login_url='index')
def Event_list(request):
    if not  request.user.login_role.filter(name='Admin').exists():
        return redirect('Error-Page')
    manager_name = Login_Role.objects.all().values_list('login_role', flat=True).distinct()
  #  project_verticals = Event_Data.objects.all().values_list('project_vertical',flat=True).distinct()


    search = request.GET.get('search')
    if search and search != 'all':
        event_list = Login_Role.objects.filter(login_role=search)
    else:
        event_list = Event_Data.objects.all()
    context = {
        'events': event_list,
        'd1': manager_name,

    }
    return render(request, 'Admin/AdminDashboard.html', context)

# def vertical_base(request):
#     project_verticals = Event_Data.objects.all().values_list('project_vertical', flat=True).distinct()
#     verticals =  request.GET.get('search_role')
#
#     if verticals and verticals != 'all':
#         project_vertical = Event_Data.objects.filter(project_vertical=verticals)
#     else:
#         project_vertical = Event_Data.objects.all()
#     context = {
#         'vertical_data': project_vertical,
#         'e1': project_verticals
#     }
#     return render(request, 'Admin/event_list.html', context)


# Error Page
def error_page(request ):
    return render(request,'Admin/components/Error_404.html',)






# Download Excel File 
@login_required(login_url='index')
def download_excel(request):
    workbook = Workbook()
    sheet = workbook.active
    sheet.title = 'Event Data'

    # Set the headers in the first row
    headers = [
        'Event Date', 'Manager Name', 'Event Name', 'Event Venue', 'Event Expense', 'Role YI', 'Project Verticals',
        'Project Stakeholder', 'YI Pillar', 'SIG', 'School', 'Collage', 'Associate Partner', 'Event Handle', 'Impact', 'Image'
    ]

    # Set the headers row
    sheet.append(headers)

    # Styling for headers (Bold and Centered)
    for cell in sheet[1]:
        cell.font = Font(bold=True)
        cell.alignment = Alignment(horizontal='center', vertical='center')

    # Get all event data
    event_data = Event_Data.objects.all()

    # Write event data rows
    for i in event_data:
        row = [
            i.date, i.your_name, i.event_name, i.event_venue, i.event_expense, i.role_yi, i.project_vertical,
            i.project_stakeholder, i.yi_pillar, i.which_SIG, i.school, i.collage, i.associate_partner,
            i.event_handle, i.total_impact
        ]
        sheet.append(row)

        # Now, for each event, if there are related images, we add them as hyperlinks.
        event_images = Event_Image.objects.filter(event=i)  # Access related Event_Image for each Event_Data

        # Initialize a list to store image URLs
        img_urls = []

        # Loop through all images for this event and generate URLs for the images
        for img in event_images:
            if img.event_photo:
                # Construct the URL for the image
                img_url = os.path.join(settings.MEDIA_URL, img.event_photo.name)
                img_urls.append(img_url)

        # Insert the URLs into the last column (Column P)
        if img_urls:
            # Concatenate all image URLs into one string, separated by commas (optional)
            image_link = ', '.join(img_urls)

            # Write the image links into the last column
            cell = f'P{sheet.max_row}'
            sheet[cell] = image_link

            # Make the cell contents a clickable link by adding the hyperlink to each image URL.
            sheet[cell].hyperlink = image_link
            sheet[cell].style = 'Hyperlink'
            sheet[cell].alignment = Alignment(wrap_text=True)

    # Adjust column widths based on content size
    for col in sheet.columns:
        max_length = 0
        column = col[0].column_letter  # Get the column name
        for cell in col:
            try:
                if len(str(cell.value)) > max_length:
                    max_length = len(cell.value)
            except:
                pass
        adjusted_width = (max_length + 2)
        sheet.column_dimensions[column].width = adjusted_width

    # Generate the response to download the file
    response = HttpResponse(
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    response['Content-Disposition'] = 'attachment; filename="Event_Data.xlsx"'

    workbook.save(response)
    return response

@login_required(login_url='index')
def manager_list(request):
    # Check if the user has the 'Admin' role
    
    try:
        if not request.user.login_role.filter(name='Admin'):
            return redirect('Error-Page')
    except Exception:
        return redirect('Error-Page')  # Redirect if the user doesn't have the Admin role
    
  

    # Make sure you're filtering by the 'user' field, not 'username'
    manager = LoginSide.objects.exclude(is_superuser=True)
    

    # Fetch all login roles (you can filter this as needed)
    login_role = Login_Role.objects.all()
    
    # Get the user's roles
    user_roles = request.user.login_role.all()

    sessions = Session.objects.filter(expire_date__gte=now())
    # Get user ids from the session data
    user_ids = [session.get_decoded().get('_auth_user_id') for session in sessions]
    # Query LoginSide objects for users
    active_users = LoginSide.objects.filter(id__in=user_ids)  # Get user objects
    
    active_user_names = [f"{user.first_name} {user.last_name}" for user in active_users]  
    active_users_count = LoginSide.objects.filter(is_active=True).count()
  
    active_users_count = active_users.count()
    
    # Prepare context to pass to the template
    context = {
        'role': login_role,
        'managers': manager,
        'user_role': user_roles,
        'count':active_users_count,
        'name':active_user_names
    }
    
    # Render the template with the context
    return render(request, 'Admin/view_manager.html', context)

# def Ec_Member(request):
#     if not request.user.login_role.filter(name='Admin').exists():
#         return redirect('Error-Page')
#     return render(request,'Admin/view_manager.html')


# Delete Ec  Member 
@login_required(login_url='index')
def delete_handler(request,handler_id):
    if not request.user.login_role.filter(name='Admin').exists():
        return redirect('Error-Page')
    if request.method == 'POST':
        handler = get_object_or_404(LoginSide, id=handler_id)
        if handler.photo:
            handler.photo.delete()
        handler.delete()
    return redirect('View-manager')



# Delete Yi Event
@login_required(login_url='index')
def delete_event(request, event_id):
    # Ensure only admins can delete events
    if not request.user.login_role.filter(name='Admin').exists():
        return redirect('Error-Page')
    try:
        
        if request.method == 'POST':
            # Get the Event_Data instance to be deleted
            event_to_delete = get_object_or_404(Event_Data, id=event_id)
            event_image = event_to_delete.event_photo.all()     
                
            for img in event_image:
                try:
                    path = img.event_photo.path
                    print(path)
                    if os.path.isfile(path):
                        os.remove(path)
                except Exception as e:
                    messages.error(request,'Error deleteing image')
                    img.delete()
                                        
            # Delete the Event_Data instance, which will also delete related Event_Image instances due to cascade
            event_to_delete.delete()
           
        # Redirect back to the Admin Dashboard after deletion
        return redirect('Admin_Dashboard')
    except Exception as e:
        messages.error(request,"Somthing went Wrong plz Try Again Event was not deleted ")

@login_required(login_url='index')
def update_memeber(request,manager_id):
    if not request.user.login_role.filter(name='Admin').exists():
        return redirect('Error-Page')
    update_manager_data = get_object_or_404(LoginSide,id=manager_id)
    try:
        
        if request.method == 'POST':
            update_manager_data.first_name = request.POST['manager_first_name']
            update_manager_data.last_name = request.POST['manager_last_name']
            update_manager_data.username = request.POST['manager_username']
            update_manager_data.yi_role = request.POST['yi_role']
            update_manager_data.email = request.POST['manager_email']
            login_roles = request.POST.getlist('login_role')
            update_manager_data.login_role.set(Login_Role.objects.filter(name__in=login_roles))# many to many filed change with set() in django

            
            # update_manager_data.password = request.POST['manager_password']
            update_manager_data.phone_number = request.POST['manager_phone_number']

            print(update_manager_data.login_role)

            if 'manager_profile_img' in request.FILES:
                update_manager_data.photo = request.FILES['manager_profile_img']

                if update_manager_data.photo.size > 4*1024*1024:
                    messages.error(request,'Image Size must be 4mb ')
                    return redirect('View-manager')
            try:

                update_manager_data.full_clean() 
                update_manager_data.save()
                messages.success(request, 'EC Member  Profile  Updated')
            
                return redirect('View-manager')
            except Exception as e:
                # print(e.message_dict.items())
                for field, errors in e.message_dict.items():
                    # print(field)
                    # print(errors)
                    for error in errors:
                        messages.error(request, f"{field}: {error}")
                    return redirect('View-manager')
            
        else:
            messages.error(request,'EC Member profile not Updated Please  Try Again')
        return redirect('View-manager')
    except Exception:
        messages.error(request,"EC Member profile not Updated Please  Try Again")
        return redirect('View-manager')


@login_required(login_url='index')
def update_event_data(request,event_id):
    if not request.user.login_role.filter(name='Admin').exists():
        return redirect('Error-Page')
    
    else:
        
        try:
            
            update_event = get_object_or_404(Event_Data, id=event_id)
            
            if request.method == 'POST':
                update_event.school  = request.POST['school']
                update_event.collage =  request.POST['collage']
                update_event.date = request.POST['event_date']
                update_event.event_name = request.POST['event_name']
                update_event.event_expense = request.POST['event_expense']
                update_event.role_yi = request.POST['role_yi']
                update_event.project_vertical = request.POST['project_verticals']
                update_event.project_stakeholder = request.POST['project_stakeholder']
                update_event.yi_pillar = request.POST['yi_pillar']
                update_event.social_link = request.POST['social_link']
                update_event.event_handle = request.POST['event_handle']
                update_event.total_impact = request.POST['total_impact']
                update_event.which_SIG = request.POST['sig_']
                update_event.associate_partner = request.POST.get('associate_partners')


                event_image = request.FILES.getlist('event_image')

                for image in event_image:
                    Event_Image.objects.create(event=update_event,event_photo = image)
                update_event.save()



                
                
              
                # event_image = request.FILES.getlist('event_image')

                # for image in event_image:
                #     Event_Image.objects.save(event_image=image,event=update_event)
                



                messages.success(request,'Event Update Successfully')
                return redirect('Admin_Dashboard')

            else:
                messages.error(request,'Event not updated')
                return redirect('Admin_Dashboard')
        except Exception:
            messages.error(request,'Something Went Wrong Please  Try Again')
            return redirect('Admmin_Dashboard')

@login_required(login_url='index')
def event_image_delete(request, image_id):
    if request.method == 'POST':
        image_to_delete = get_object_or_404(Event_Image, id=image_id)
        if image_to_delete.event_photo:
            image_to_delete.event_photo.delete()
        image_to_delete.delete()  # Delete the image record
    return redirect('Admin_Dashboard')

#  if delete_event.event_photo():
#             delete_event.event_photo.delete()
            
#         delete_events.delete()


#@method_decorator(login_required(login_url='index'),name='get')





class EventDataAPI(APIView):
    def get(self, request):
        event = Event_Data.objects.all()
        serializers = EventDataSerializer(event, many=True)
        return Response(serializers.data)

    def post(self, request):
        # Create a new Event_Data object
        serializers = EventDataSerializer(data=request.data)
        if serializers.is_valid():
            serializers.save()  # Save the new object
            return Response(serializers.data)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        # Ensure the 'id' is passed and object exists
        try:
            # event_id = request.query_params.get('id')
            # event = Event_Data.objects.get(pk=request.data.get('id'))
            event= Event_Data.request.query_params.get('id')
            event.delete()  # Delete the object

            return Response({'message': 'Event deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
        except Event_Data.DoesNotExist:
            return Response({'error': 'Event not found'}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request):

        # Get the event instance based on the provided ID
        event = Event_Data.objects.get(pk=request.data.get('id'))

        # Pass the event instance and updated data to the serializer
        serializer = EventDataSerializer(event, data=request.data, partial=False)

        # Validate and save the data
        if serializer.is_valid():
            serializer.save()  # Save the updated event
            return Response(serializer.data)  # Return the updated data
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




# Admin Side Chart 

def admin_chart(request):
    event_data = Event_Data.objects.all().values_list('your_name', flat=True).distinct()
    # event_impact = Event_Data.objects.all().values_list('total_impact',flat=True).annotate(Sum('total_impact'))
    event_impact_by_name = Event_Data.objects.values('your_name').annotate(total_impact=Sum('total_impact')).order_by('your_name')


    project_verticals = Event_Data.objects.all().values_list('project_vertical', flat=True).distinct()
    # event_impact = Event_Data.objects.all().values_list('total_impact',flat=True).annotate(Sum('total_impact'))
    project_verticals_by_name = Event_Data.objects.values('your_name').annotate(total_impact=Sum('project_vertical')).order_by('project_vertical')


    context = {
        'name': event_data,
        'impact_data':event_impact_by_name,
        'verticals':project_verticals,
       
    }
    return render(request, 'Admin/chart/admin_chart.html', context)

# matplotlib.use('Agg')
# def plot_chart(request):
#     # Get all event data
#     event = Event_Data.objects.all()
#     total_event = Event_Data.objects.count()
#
#     # Collecting 'your_name' from Event_Data model
#     x = [i.your_name for i in event]
#
#     # Count how many events each person has done
#     event_counts = Counter(x)
#
#     # Create the plot
#     plt.figure(figsize=(8, 5))
#
#     # Get the unique names and their corresponding event counts
#     unique_names = list(event_counts.keys())
#     event_numbers = list(event_counts.values())
#
#     # Plot the bar chart
#     plt.bar(unique_names, event_numbers)
#
#     # Function to add labels on top of the bars showing the number of events
#     def addlabels(event_counts):
#         for i, count in enumerate(event_numbers):
#             plt.text(i, count + 0.1, str(count), ha='center', fontsize=10)
#
#     # Call the addlabels function
#     addlabels(event_counts)
#
#
#     plt.title(f" Total Events: {total_event}", fontsize=23, color='red', fontname='cambria')
#     plt.xlabel("Names")
#     plt.ylabel("Event Count")
#
#     # Rotate x-axis labels for better readability
#
#
#     # Add total event count in a text box on the plot
#     plt.text(0.5, max(event_numbers) * 1.05, f'Total Events: {total_event}', ha='center', fontsize=12, color='blue',
#              transform=plt.gca().transAxes)
#
#     plt.legend(["Total"])
#
#     # Save the plot to a BytesIO object
#     buffer = BytesIO()
#     plt.savefig(buffer, format='jpg')
#     buffer.seek(0)
#
#     # Close the plot to avoid memory issues when running multiple plots
#     plt.close()
#     # Return the image as an HttpResponse with the correct content type
#     return HttpResponse(buffer, content_type='image/jpg')



# def pie_chart(request):
#     event = Event_Data.objects.all()
#
#     # Collecting 'total_impact' and 'date' fields
#     impact = np.array([i.total_impact for i in event])
#     names = [i.date.strftime('%D') for i in event]  # Format dates to strings for better readability
#
#     # Create the pie chart
#     plt.figure(figsize=(8, 5))
#     plt.pie(impact, labels=names, autopct='%1.1f%%', )
#
#     # Set the title of the plot
#     plt.title('Impact Distribution by Event Date', fontsize=16, fontname='Cambria')
#
#     # Save the plot to a BytesIO object
#     buffer = BytesIO()
#     plt.savefig(buffer, format='jpg')
#     buffer.seek(0)
#
#     # Close the plot to avoid memory issues
#     plt.close()
#
#     # Return the image as an HTTP response
#     return HttpResponse(buffer, content_type='image/jpg')
#
# #
# # def line_chart(request):
# #     event = Event_Data.objects.all()
# #     event_date = np.array([i.date for i in event])

# ForgotPasssword Side 
class CustomPasswordResetView(PasswordResetView):
    template_name = 'password/password_reset_form.html'
    email_template_name = 'password/password_reset_email.html'
    success_url = reverse_lazy('password_reset_done')

class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'password/password_reset_done.html'

class CustomPasswordResetConfirm(PasswordResetConfirmView):
    template_name = 'password/password_reset_confirm.html'
    success_url = reverse_lazy('password_reset_complete')

def password_update_done(request):
    return render(request,'Admin/components/password_update_done.html')


# def update_manager(request, manager_id):
#     if not request.user.login_role.filter(name='Admin').exists():
#         return redirect('Error-Page')
    
#     update_manager_data = get_object_or_404(LoginSide, id=manager_id)
    
#     if request.method == 'POST':
#         update_manager_data.first_name = request.POST['manager_first_name']
#         update_manager_data.last_name = request.POST['manager_last_name']
#         update_manager_data.username = request.POST['manager_username']
#         update_manager_data.email = request.POST['manager_email']
        
#         # Assuming you want to update the login roles
#         login_roles = request.POST.getlist('login_role')  # This is a list of role IDs
#         update_manager_data.login_role.set(Login_Role.objects.filter(name__in=login_roles))  # Set roles by filtering by IDs
        
#         update_manager_data.phone_number = request.POST['manager_phone_number']

#         # Optional: Updating the profile image
#         if 'manager_profile_img' in request.FILES:
#             update_manager_data.photo = request.FILES['manager_profile_img']

#         # Check if the image is too large
#         if update_manager_data.photo.size > 4 * 1024 * 1024:
#             messages.error(request, 'Image Size must be 4mb ')
#             return redirect('View-manager')

#         update_manager_data.save()
#         messages.success(request, 'Manager profile updated')

#     else:
#         messages.error(request, 'Manager profile not updated')
    
#     return redirect('View-manager')


# def delete_multiple_events(request):
#     # Fetch all events from the database
#     events = Event_Data.objects.all()

#     # Handle the form submission
#     if request.method == 'POST':
#         # Check if the delete button was clicked
#         if 'delete_events' in request.POST:
#             selected_event_ids = request.POST.getlist('selected_events')

#             if selected_event_ids:
#                 # Delete selected events
#                 demo =Event_Data.objects.filter(id__in=selected_event_ids)


#             # After deletion, redirect to the same page (or elsewhere)
#             return redirect('Admin_Dashboard')  # Replace with your actual view name

#     return render(request, 'Admin/AdminDashboard.html', {'events': events})












#warning: in the working copy of 'day/admin_app/views.py', LF will be replaced by CRLF the next time Git touches it





# person = Person.objects.get(email="example@example.com")L



# from django.db import models
# from django.contrib.auth.models import AbstractUser
# import uuid
# from django.core.exceptions import ValidationError
# import re

# # Custom validator for email domain
# def validate_email_domain(value):
#     if '@example.com' not in value:
#         raise ValidationError('Email must be from the domain @example.com')

# # Custom validator for phone number
# def validate_phone_number(value):
#     # Ensure phone number contains only digits
#     if not value.isdigit():
#         raise ValidationError('Phone number must contain only digits')
#     # Optionally, you can add checks for length or specific formats
#     if len(value) < 10 or len(value) > 15:
#         raise ValidationError('Phone number must be between 10 and 15 digits')

# # Assuming Login_Role is already defined somewhere
# class Login_Role(models.Model):
#     role_name = models.CharField(max_length=200)

# class LoginSide(AbstractUser):
#     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, db_index=True)
#     login_role = models.ManyToManyField(Login_Role)
#     first_name = models.CharField(max_length=200, null=True)
#     last_name = models.CharField(max_length=200)
#     email = models.EmailField(max_length=200, unique=True, validators=[validate_email_domain])  # Added email validator
#     photo = models.ImageField(upload_to='user_photo/', null=True)
#     yi_role = models.CharField(max_length=200, null=True)
    
#     # Updated phone number to CharField with validator
#     phone_number = models.CharField(max_length=15, default='0', null=True, blank=True, validators=[validate_phone_number])  # Added phone number validator

#     def __str__(self):
#         return self.username

# value = float(value)
#         if value >= 1000:
#             return f"{value / 1000:.0f}K"
#         return str(value)







