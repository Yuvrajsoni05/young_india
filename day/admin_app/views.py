# Standard library imports
import os
import re
from collections import Counter


# Django imports
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login, authenticate, update_session_auth_hash, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.views import (
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
)
from django.contrib.sessions.models import Session
from django.core.paginator import Paginator
from django.core.validators import FileExtensionValidator, ValidationError
from django.db.models import Avg, Sum
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.templatetags.static import static
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.utils.timezone import now
from django.views.decorators.cache import never_cache

from babel.numbers import format_currency

# Third-party imports
# from io import BytesIO
import numpy as np
from PIL.Image import Image
from asgiref.typing import HTTPResponseBodyEvent
from matplotlib import pyplot as plt
from openpyxl import Workbook
from openpyxl.styles import Alignment, Font
from openpyxl.drawing.image import Image

# import matplotlib
# import logging

import openpyxl

# from PIL import Image as PILImage

# DRF imports
from rest_framework import status
from rest_framework.response import Response
from rest_framework.reverse import reverse_lazy
from rest_framework.views import APIView

# Local imports
from .models import *
from manager_app.models import Event_Data, Event_Image
from .serializer import EventDataSerializer


from django.utils.decorators import decorator_from_middleware
from django.middleware.cache import CacheMiddleware
from django.views.decorators.cache import cache_control, never_cache


from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
# Create your views here.


def  check_role(view_func):
    def wrapper(request,*args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('index')
        if not request.user.yi_role == 'Chapter Co-Chair' or request.euser.yi_role == 'Chapter Chair' or request.user.yi_role == 'Admin' :
            return redirect('Error-Page')
        return view_func(request,*args,**kwargs)
    return wrapper



@never_cache
@cache_control(no_store=True, no_cache=True, must_revalidate=True, max_age=0)
def index(request):
    try:
        if request.method == "POST":
            username = request.POST.get("username")
            password = request.POST.get("password")

            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)  # Log the user in

                # if user.login_role.filter(name="Admin").exists():
                #     # print(f"{username} , {password}")
                #     # logger.info(f"Someone is trying to login Name : {username} {password}")
                if user.yi_role == 'Chapter Co-Chair' or user.yi_role == 'Chapter Chair' or user.yi_role == 'Admin' :
                    return redirect("Admin_Dashboard")
                elif user.yi_role == 'Branding':
                    return redirect("branding_dashboard")
                else:
                    roles = user.login_role.all()
                    request.session["userrole"] = [role.name for role in roles]
                    if roles.exists():
                        first_role_with_image = roles.filter(
                            image__isnull=False
                        ).first()
                        if first_role_with_image:
                            request.session["image"] = first_role_with_image.image.url
                        else:
                            request.session["image"] = "No Image"
                    # Get all roles associated with the user
                    return redirect("member-dashbaord")
            else:
                messages.error(request, "Invalid credentials, please try again.")
                # logger.info(f"Error during authentication: {str(e)}")
                return redirect("index")
    except Exception as e:

        messages.error(request, f"Error")
    return render(request, "index.html")


# Add new User Ec members

@never_cache
@cache_control(no_store=True, no_cache=True, must_revalidate=True, max_age=0)
@login_required(login_url="index")
def Admin_Signup(request):
    if request.user.yi_role not in ['Chapter Co-Chair', 'Chapter Chair', 'Admin']:
            return redirect("Error-Page")

    sessions = Session.objects.filter(expire_date__gte=now())
    # Get user ids from the session data
    user_ids = [session.get_decoded().get("_auth_user_id") for session in sessions]
    # Query LoginSide objects for users
    active_users = LoginSide.objects.filter(id__in=user_ids)  # Get user objects
    active_user_names = [f"{user.first_name} {user.last_name}" for user in active_users]
    active_users_count = active_users.count()
    login_roles = Login_Role.objects.all()

    try:
        if request.method == "POST":
            username = request.POST.get("add_username")
            first_name = request.POST.get("first_name")
            last_name = request.POST.get("last_name")
            password = request.POST.get("password1")
            profile_img = request.FILES.get("profile_img")
            confirm_password = request.POST.get("password2")
            Admin_email = request.POST.get("add_email")
            phone = request.POST.get("add_phone")
            yi_role = request.POST.get("yi_role")
            login_role = request.POST.getlist(
                "login_role"
            )  # Use getlist to fetch multiple roles

            required_fields = {
                "Username": username,
                "First Name": first_name,
                "Last Name": last_name,
                "Email": Admin_email,
                "Phone": phone,
                "Yi Role": yi_role,
                # "EC Role": login_role,
                "Password": password,
                "Confirm Password": confirm_password,
            }

            form_data = {
                "username": username,
                "first_name": first_name,
                "last_name": last_name,
                "email": Admin_email,
                "phone": phone,
                "yi_role": yi_role,
                # "login_role": login_role,
            }

            if "resetbutton" in request.POST:
                return render(
                    request,
                    "Admin/AdminSignup.html",
                    {
                        "role": login_roles,
                        "name": active_user_names,
                        "count": active_users_count,
                        "form_data": {},
                    },
                )

            # Validation for required fields
            for field, field_value in required_fields.items():
                if not field_value:
                    messages.error(request, f"The {field} field is required")
                    return render(
                        request,
                        "Admin/AdminSignup.html",
                        {
                            "role": login_roles,
                            "name": active_user_names,
                            "count": active_users_count,
                            "form_data": form_data,
                        },
                    )

            # Profile image handling
            if profile_img:
                try:
                    validator = FileExtensionValidator(
                        allowed_extensions=["jpeg", "jpg", "png"]
                    )
                    validator(profile_img)
                except ValidationError:
                    messages.error(
                        request, "Invalid file type. Only .jpeg, .jpg, .png allowed."
                    )
                    return render(
                        request,
                        "Admin/AdminSignup.html",
                        {
                            "role": login_roles,
                            "name": active_user_names,
                            "count": active_users_count,
                            "form_data": form_data,
                        },
                    )

                if profile_img.size > 10 * 1024 * 1024:  # 10 MB limit
                    messages.error(request, "Image size must be less than 10 MB.")
                    return render(
                        request,
                        "Admin/AdminSignup.html",
                        {
                            "role": login_roles,
                            "name": active_user_names,
                            "count": active_users_count,
                            "form_data": form_data,
                        },
                    )
            # You should adjust this according to your model's field default.

            # Email and phone validation
            email_regex = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
            if not re.match(email_regex, Admin_email):
                messages.error(request, "Enter a valid email address.")
                return render(
                    request,
                    "Admin/AdminSignup.html",
                    {
                        "role": login_roles,
                        "name": active_user_names,
                        "count": active_users_count,
                        "form_data": form_data,
                    },
                )

            if LoginSide.objects.filter(email=Admin_email).exists():
                messages.error(request, "This email is already taken.")
                return render(
                    request,
                    "Admin/AdminSignup.html",
                    {
                        "role": login_roles,
                        "name": active_user_names,
                        "count": active_users_count,
                        "form_data": form_data,
                    },
                )

            regex = r"^(\+91[\-\s]?)?[0]?(91)?[789]\d{9}$"
            if not re.match(regex, phone):
                messages.error(request, "Phone number must be 10 digits and valid.")
                return render(
                    request,
                    "Admin/AdminSignup.html",
                    {
                        "role": login_roles,
                        "name": active_user_names,
                        "count": active_users_count,
                        "form_data": form_data,
                    },
                )

            if (
                len(password) < 8
                or not any(c.isupper() for c in password)
                or not any(c in "!@#$%^&*()_+-={}[]\\:;\"'<>,.?/~`" for c in password)
            ):
                messages.error(
                    request,
                    "Password must be at least 8 characters with one uppercase letter and one special character.",
                )
                return render(
                    request,
                    "Admin/AdminSignup.html",
                    {
                        "role": login_roles,
                        "name": active_user_names,
                        "count": active_users_count,
                        "form_data": form_data,
                    },
                )

            if password != confirm_password:
                messages.error(request, "Password and confirm password must match.")
                return render(
                    request,
                    "Admin/AdminSignup.html",
                    {
                        "role": login_roles,
                        "name": active_user_names,
                        "count": active_users_count,
                        "form_data": form_data,
                    },
                )
            
            # Create user
            Admin_User = LoginSide.objects.create_user(
                username=username,
                first_name=first_name,
                last_name=last_name,
                photo=profile_img,
                password=password,
                email=Admin_email,
                yi_role=yi_role,
                phone_number=phone,
            )
            
            # user_info = {
            #         "username": username,
            #         "password": password,
            #         "yi_role": yi_role,
            #         "login_role": login_role,
                    
            # }
            
            # receiver_email =  Admin_email
            # template_name = "base/email.html"

            # convert_to_html_content =  render_to_string(
            # template_name=template_name,
            # context=user_info
            
          
            # )
            # plain_message = strip_tags(convert_to_html_content)
            # send_mail(
            #       subject=  'Hello Ec Member',
            #         message=plain_message,
            #         from_email= request.user.email,
            #         recipient_list=[receiver_email],
            #         html_message=convert_to_html_content,
            #         fail_silently=False,
            #     )
            
  
            

            # Assign selected roles to the user
            roles = Login_Role.objects.filter(
                name__in=login_role
            )  # Filter roles based on selected ones
            Admin_User.login_role.set(roles)  # Assign multiple roles

            Admin_User.full_clean()
            Admin_User.save()
            messages.success(request, "New Executive Council Member Added")
            return redirect("Admin_Signup")

        return render(
            request,
            "Admin/AdminSignup.html",
            {
                "role": login_roles,
                "name": active_user_names,
                "count": active_users_count,
            },
        )

    except Exception as e:
        messages.error(request, f"An error occurred: {str(e)}")
        return render(
            request,
            "Admin/AdminSignup.html",
            {
                "role": login_roles,
                "name": active_user_names,
                "count": active_users_count,
            },
        )


# Admin Profie  HTML Page


@never_cache
@cache_control(no_store=True, no_cache=True, must_revalidate=True, max_age=0)
@login_required(login_url="index")
def Admin_Profile(request):
    if request.user.yi_role not in ['Chapter Co-Chair', 'Chapter Chair', 'Admin','Branding']:
            return redirect("Error-Page")

    sessions = Session.objects.filter(expire_date__gte=now())
    # Get user ids from the session data
    user_ids = [session.get_decoded().get("_auth_user_id") for session in sessions]
    # Query LoginSide objects for users
    active_users = LoginSide.objects.filter(id__in=user_ids)  # Get user objects

    active_user_names = [f"{user.first_name} {user.last_name}" for user in active_users]
    active_users_count = LoginSide.objects.filter(is_active=True).count()

    active_users_count = active_users.count()
    context = {
        "name": active_user_names,
        "count": active_users_count,
    }
    return render(request, "Admin/Admin_Profile.html", context)


# Admin profile Update View Code

@never_cache
@cache_control(no_store=True, no_cache=True, must_revalidate=True, max_age=0)
@login_required(login_url="index")
def Admin_update(request, admin_id):
    # Check if the user has 'Admin' role
    if request.user.yi_role not in ['Chapter Co-Chair', 'Chapter Chair', 'Admin','Branding']:
            return redirect("Error-Page")

    try:
        if request.method == "POST":
            first_name = request.POST["admin_firstname"]
            last_name = request.POST["admin_lastname"]
            username = request.POST["admin_username"]
            # yi_role = request.POST['yi_role']
            email = request.POST["admin_email"]
            # login_role = request.POST.getlist('login_role')
            phone_number = request.POST["admin_phone"]

        required_fields = {
            "First Name": first_name,
            "Last Name": last_name,
            "Username": username,
            "Email": email,
            "Phone Number": phone_number,
        }

        for field, field_value in required_fields.items():
            if not field_value:
                messages.error(request, f"The {field} field is Required ")
                return redirect("Admin_Profile")

        # Ensure method is POST to update profile
        if request.method == "POST":
            admin_profile = get_object_or_404(LoginSide, id=admin_id)

            # Update fields from POST data
            admin_profile.first_name = first_name
            admin_profile.last_name = last_name
            admin_profile.email = email
            admin_profile.username = username
            admin_profile.phone_number = phone_number

            if "admin_profile_img" in request.FILES:

                if admin_profile.photo.size > 10 * 1024 * 1024:
                    messages.error(request, "Image size must be less than 10 MB ")
                    return redirect("Admin_Profile")

                if (
                    admin_profile.photo
                    and hasattr(admin_profile.photo, "path")
                    and os.path.exists(admin_profile.photo.path)
                ):
                    print(admin_profile.photo.path)
                    os.remove(admin_profile.photo.path)

                admin_profile.photo = request.FILES["admin_profile_img"]

                if admin_profile.photo:
                    try:
                        validator = FileExtensionValidator(
                            allowed_extensions=["jpeg", "jpg", "png"]
                        )
                        validator(admin_profile.photo)
                    except ValidationError:
                        messages.error(
                            request,
                            "Invalid file type. Only .jpeg, .jpg, .png allowed.",
                        )
                        return redirect("Admin_Profile")

            try:
                admin_profile.full_clean()
                admin_profile.save()
                messages.success(request, "Profile successfully updated.")
                return redirect("Admin_Profile")
            except Exception as e:
                for field, errors in e.message_dict.items():
                    for error in errors:
                        messages.error(request, f"{error} ")
                    return redirect("Admin_Profile")
        # If the method is not POST, show an error

    except Exception as e:
        # Handle any other errors during the process
        messages.error(request, f"Error updating profile: {str(e)}")
        return redirect("Admin_Profile")


# Admin password  Update


@never_cache
@cache_control(no_store=True, no_cache=True, must_revalidate=True, max_age=0)
@login_required(login_url="index")
def admin_password(request):
    if request.user.yi_role not in ['Chapter Co-Chair', 'Chapter Chair', 'Admin' ,'Branding']:
            return redirect("Error-Page")
    else:
        
        try:

            if request.method == "POST":
                old_password = request.POST.get("old_password")
                new_password = request.POST.get("new_password")
                confirm_password = request.POST.get("confirm_password")
                admin_user = request.user
                if not admin_user.check_password(old_password):
                    messages.error(request, "Old Password Incorrect")
                    return redirect("Admin_Profile")

                if (
                    len(new_password) < 8
                    or not any(c.isupper() for c in new_password)
                    or not any(
                        c in "!@#$%^&*()_+-={}[]\\:;\"'<>,.?/~`" for c in new_password
                    )
                ):
                    messages.error(
                        request,
                        "Password must be at least 8 characters with one uppercase letter and one special character",
                    )
                    return redirect("Admin_Profile")

                if new_password != confirm_password:
                    messages.error(
                        request, "New Password and Confirm Password must Be same"
                    )
                    return redirect("Admin_Profile")

                admin_user.set_password(new_password)
                admin_user.save()
                messages.success(request, "Password Updated ")
                update_session_auth_hash(request, admin_user)
                return redirect("Admin_Profile")
            else:
                return redirect("Error-Page")
        except Exception as e:
            messages.error(request, "Somthing Wrong ", str(e))


# Admin Logout


@never_cache
@cache_control(no_store=True, no_cache=True, must_revalidate=True, max_age=0)
@login_required(login_url="index")
def admin_logout(request):
    logout(request)
    request.session.clear()
    return redirect("index")


# Admin Dashboard
@never_cache
@cache_control(no_store=True, no_cache=True, must_revalidate=True, max_age=0)
@login_required(login_url="index")
def Admin_Dashboard(request):

    if request.user.yi_role not in ['Chapter Co-Chair', 'Chapter Chair', 'Admin']:
        return redirect("Error-Page")
    
    # You don't need to reassign user_id since it's already passed in the URL
    total_event = Event_Data.objects.count()
    user_id = request.user.id
    total_user_data = LoginSide.objects.exclude(login_role="Admin")
    total_user = total_user_data.count()
    sessions = Session.objects.filter(expire_date__gte=now())
    # Get user ids from the session data
    user_ids = [session.get_decoded().get("_auth_user_id") for session in sessions]
    # Query LoginSide objects for users
    active_users = LoginSide.objects.filter(id__in=user_ids)  # Get user objects

    active_user_names = [f"{user.first_name} {user.last_name}" for user in active_users]
    active_users_count = LoginSide.objects.filter(is_active=True).count()
    active_users_count = active_users.count()
    total_expense_result = Event_Data.objects.aggregate(Sum("event_expense"))
    total_expense = (
        total_expense_result["event_expense__sum"]
        if total_expense_result["event_expense__sum"] is not None
        else 0
    )
    total_impact_result = Event_Data.objects.aggregate(Sum("total_impact"))
    total_impact = (
        total_impact_result["total_impact__sum"]
        if total_impact_result["total_impact__sum"] is not None
        else 0
    )
    impact_avg = Event_Data.objects.aggregate(Avg("total_impact"))
    avg_impact = (
        impact_avg["total_impact__avg"]
        if impact_avg["total_impact__avg"] is not None
        else 0
    )
    # Retrieve all distinct users and roles
    all_user = LoginSide.objects.all().distinct()
    login_role = Login_Role.objects.all().distinct()

    def formatINR(total_expense):
        s, *d = str(total_expense).partition(".")
        r = ",".join([s[x - 2 : x] for x in range(-3, -len(s), -2)][::-1] + [s[-3:]])
        return "".join([r] + d)

    

    def formatImpact(total_impact):
        s, *d = str(total_impact).partition(".")
        r = ",".join([s[x - 2 : x] for x in range(-3, -len(s), -2)][::-1] + [s[-3:]])
        return "".join([r] + d)

    

    # Manager names from Event_Data
    imapct = (Event_Data.objects.all().values_list('total_impact',flat=True))
    
    member_name = (
        Event_Data.objects.all().values_list("your_name", flat=True).distinct()
    )
    vertical_name = (
        Event_Data.objects.all().values_list("project_vertical", flat=True).distinct()
    )
    stakeholder_name = (
        Event_Data.objects.all()
        .values_list("project_stakeholder", flat=True)
        .distinct()
    )
    yi_pillar_name = (
        Event_Data.objects.all().values_list("yi_pillar", flat=True).distinct()
    )
    event_date = (
        Event_Data.objects.all().values_list("date",flat=True).distinct()
    )
    yi_role_name = Event_Data.objects.all().values_list("role_yi", flat=True).distinct()
    total_vertical = vertical_name.count()
    # event_list = Event_Data.objects.all()

    member_name_chart = (
        Event_Data.objects.all().values_list("your_name", flat=True).distinct()
    )
    vertical_name_chart = (
        Event_Data.objects.all().values_list("project_vertical", flat=True)
    )
    imapct_chart = (Event_Data.objects.all().values_list('total_impact',flat=True))


    event_list = Event_Data.objects.all()

    vertical_chart = [event for event in vertical_name_chart ]
    impact_chart = [event for event in  imapct_chart]
    member_chart = [event for event in  member_name_chart]
    
    # def event_chart(request):
    # events = Event.objects.all()
    # labels = [event.event_name for event in events]
    # data = [event.event_impact for event in events]
    # context = {
    #     'labels': labels,
    #     'data': data,
    # }

    selected_vertical = request.GET.get("vertical", "all")
    if selected_vertical != "all":
        total_vertical = Event_Data.objects.filter(
            project_vertical=selected_vertical
        ).count()
        event_list = event_list.filter(project_vertical__icontains=selected_vertical)
        total_expense_result = event_list.aggregate(Sum("event_expense"))
        total_impact_result= event_list.aggregate(Sum("total_impact"))       
        total_impact = (total_impact_result["total_impact__sum"]if total_impact_result["total_impact__sum"] is not None
        else 0 )
        total_expense = (
            total_expense_result["event_expense__sum"]
            if total_expense_result["event_expense__sum"] is not None
            else 0
        )
        

    ec_name = request.GET.get("ec_name", "all")
    if ec_name and ec_name != "all":
        event_list = event_list.filter(your_name__icontains=ec_name)
        total_event = event_list.filter(your_name__icontains=ec_name).count
        total_impact_result= event_list.aggregate(Sum("total_impact"))       
        total_impact = (total_impact_result["total_impact__sum"]if total_impact_result["total_impact__sum"] is not None
        else 0 )
        total_expense_result = event_list.aggregate(Sum("event_expense"))
        total_expense = (
            total_expense_result["event_expense__sum"]
            if total_expense_result["event_expense__sum"] is not None
            else 0
        )
        
        
        

    verticals = request.GET.get("verticals")
    if verticals and verticals != "all":
        event_list = event_list.filter(project_vertical__icontains=verticals)
        total_event = event_list.filter(project_vertical__icontains=verticals).count()
        total_impact_result= event_list.aggregate(Sum("total_impact"))       
        total_impact = (total_impact_result["total_impact__sum"]if total_impact_result["total_impact__sum"] is not None
        else 0 )
        total_expense_result = event_list.aggregate(Sum("event_expense"))
        total_expense = (
            total_expense_result["event_expense__sum"]
            if total_expense_result["event_expense__sum"] is not None
            else 0
        )

    yi_pillar = request.GET.get("yi_pillar")
    if yi_pillar and yi_pillar != "all":
        event_list = event_list.filter(yi_pillar__icontains=yi_pillar)
        total_event = event_list.filter(yi_pillar__icontains=yi_pillar).count()
        total_impact_result= event_list.aggregate(Sum("total_impact"))       
        total_impact = (total_impact_result["total_impact__sum"]if total_impact_result["total_impact__sum"] is not None
        else 0 )
        total_expense_result = event_list.aggregate(Sum("event_expense"))
        total_expense = (
            total_expense_result["event_expense__sum"]
            if total_expense_result["event_expense__sum"] is not None
            else 0
        )

    stakeholder = request.GET.get("stakeholder")
    if stakeholder and stakeholder != "all":
        event_list = event_list.filter(project_stakeholder__icontains=stakeholder)
        total_event = event_list.filter(project_stakeholder__icontains=stakeholder).count()
        total_impact_result= event_list.aggregate(Sum("total_impact"))       
        total_impact = (total_impact_result["total_impact__sum"]if total_impact_result["total_impact__sum"] is not None
        else 0 )
        total_expense_result = event_list.aggregate(Sum("event_expense"))
        total_expense = (
            total_expense_result["event_expense__sum"]
            if total_expense_result["event_expense__sum"] is not None
            else 0
        )

    yi_role = request.GET.get("yi_role")
    if yi_role and yi_role != "all":
        event_list = event_list.filter(role_yi__icontains=yi_role)
        total_event = event_list.filter(role_yi__icontains=yi_role).count()
        total_impact_result= event_list.aggregate(Sum("total_impact"))       
        total_impact = (total_impact_result["total_impact__sum"]if total_impact_result["total_impact__sum"] is not None
        else 0 )
        total_expense_result = event_list.aggregate(Sum("event_expense"))
        total_expense = (
        total_expense_result["event_expense__sum"]
        if total_expense_result["event_expense__sum"] is not None
        else 0
    )

    date = request.GET.get("event_date")
    if date and date != "all": 
        event_list = event_list.filter(date__icontains=date)
        total_event = event_list.filter(date__icontains=date).count()
        total_impact_result= event_list.aggregate(Sum("total_impact"))       
        total_impact = (total_impact_result["total_impact__sum"]if total_impact_result["total_impact__sum"] is not None
        else 0 )
        total_expense_result = event_list.aggregate(Sum("event_expense"))
        total_expense = (
            total_expense_result["event_expense__sum"]
            if total_expense_result["event_expense__sum"] is not None
            else 0
        )
    total_impact = formatImpact(total_impact)
    total_expense = formatINR(total_expense)
    context = {
        "user_id": user_id,
        "users_data": all_user,
        "role": login_role,
        "total_manager": total_user,
        "total_event": total_event,
        "total_impact": total_impact,
        "impact_avg": avg_impact,
        "total_expense": total_expense,
        "events": event_list,
        "member_name": member_name,
        "verticals": vertical_name,
        "stakeholder": stakeholder_name,
        "yi_pillar": yi_pillar_name,
        "yi_role": yi_role_name,
        "total_vertical": total_vertical,
        "count": active_users_count,
        "name": active_user_names,
        "event_date":event_date,
        'vertical_chart':vertical_chart,
        'impact_chart':impact_chart,
        'member_chart':member_chart,
        
    }
    return render(request, "Admin/AdminDashboard.html", context)


# Base file

@never_cache
@cache_control(no_store=True, no_cache=True, must_revalidate=True, max_age=0)
@login_required(login_url="index")
def base(request):
    sessions = Session.objects.filter(expire_date__gte=now())
    # Get user ids from the session data
    user_ids = [session.get_decoded().get("_auth_user_id") for session in sessions]
    # Query LoginSide objects for users
    active_users = LoginSide.objects.filter(id__in=user_ids)  # Get user objects
    active_user_names = [f"{user.first_name} {user.last_name}" for user in active_users]
    active_users_count = LoginSide.objects.filter(is_active=True).count()
    active_users_count = active_users.count()
    context = {"count": active_users_count, "name": active_user_names}
    return render(request, "base/base.html", context)


# Admin Side Event Data

@never_cache
@cache_control(no_store=True, no_cache=True, must_revalidate=True, max_age=0)
@login_required(login_url="index")
def admin_event_data(request):

    if request.user.yi_role not in ['Chapter Co-Chair', 'Chapter Chair', 'Admin']:
        return redirect("Error-Page")


    ec_member = LoginSide.objects.all().exclude(is_superuser=True)
    ec_member_names = [
        f"{member.first_name} {member.last_name}" for member in ec_member.distinct()
    ]
    sessions = Session.objects.filter(expire_date__gte=now())
    user_ids = [session.get_decoded().get("_auth_user_id") for session in sessions]
    active_users = LoginSide.objects.filter(id__in=user_ids)
    active_user_names = [f"{user.first_name} {user.last_name}" for user in active_users]
    active_users_count = active_users.count()  # Use this count

    try:
        if request.method == "POST":

            event_name = request.POST["event_name"]
            project_vertical = request.POST["project_verticals"]
            project_stakeholder = request.POST["project_stakeholder"]
            yipiller = request.POST["yi_pillar"]
            total_impact = request.POST["total_impact"]
            event_date = request.POST["event_date"]
            yirole = request.POST["role_yi"]
            your_name = request.POST["your_name"]
            sig_option = request.POST.get("sig_", "")
            event_member = request.POST["event_member"]
            select_ec_member = request.POST.get("select_member", "")
            social_link = request.POST["social_link"]
            event_expense = request.POST["event_expense"]
            event_venue = request.POST["event_venue"]
            school = request.POST["school"]
            collage = request.POST["collage"]
            associate_partner = request.POST.get("associate_partner", "")
            event_image = request.FILES.getlist("event_img")
            event_description = request.POST.get('event_description')

            if event_expense == "":
                event_expense = 0

            required_fields = {
                "Event Date": event_date,
                "Event Name": event_name,
                "Project Vertical": project_vertical,
                "Project Stakeholder": project_stakeholder,
                "Yi Piller": yipiller,
                "Yi Role": yirole,
                "Total Impact": total_impact,
            }
            for field, field_value in required_fields.items():

                if not field_value:
                    messages.error(request, f" The  {field} field is Required")
                    return redirect("admin_event_data")

            # if len(event_image) > 6 and event_image:
            #     messages.error(request, "You can Upload only 6 Image")
            #     return redirect("admin_event_data")

            valid_extension = [".jpeg", ".jpg", ".png"]

            for img in event_image:
                ext = os.path.splitext(img.name)[1]
                if ext.lower() not in valid_extension:
                    messages.error(
                        request,
                        f"Invalid file type: {img.name} . Only .jpg, .jpeg, and .png are allowed.",
                    )
                    return redirect("admin_event_data")

            event_data = Event_Data.objects.create(
                your_name=your_name,
                date=event_date,
                role_yi=yirole,
                event_member=event_member,
                project_vertical=project_vertical,
                which_SIG=sig_option,
                project_stakeholder=project_stakeholder,
                yi_pillar=yipiller,
                social_link=social_link,
                event_venue=event_venue,
                event_expense=event_expense,
                school=school,
                collage=collage,
                total_impact=total_impact,
                event_name=event_name,
                associate_partner=associate_partner,
                select_ec_member=select_ec_member,
                event_description=event_description,
                
                user=request.user,
            )
            for image in event_image:
                Event_Image.objects.create(event_photo=image, event=event_data)

            messages.success(request, "Thank you Insert Data  ")
            return redirect("Admin_Dashboard")
        context = {
            "count": active_users_count,
            "name": active_user_names,
            "ec_member": ec_member_names,
        }

        return render(request, "Admin/Admin_Event_data.html", context)
    except Exception:
        messages.error(request, "Somthing Went  Please  Try Again")
        return redirect("Admin_Dashboard")


# Error Page
@never_cache
@cache_control(no_store=True, no_cache=True, must_revalidate=True, max_age=0)
def error_page(request):
    return render(
        request,
        "Admin/components/Error_404.html",
    )


# Download Excel File
@never_cache
@cache_control(no_store=True, no_cache=True, must_revalidate=True, max_age=0)
@login_required(login_url="index")
def download_excel(request):
    workbook = Workbook()
    sheet = workbook.active
    sheet.title = "Event Data"

    # Set the headers in the first row
    headers = [
        "Event Date",
        "Ec Members Name",
        "Event Name",
        "Event Venue",
        "Event Expense",
        "Role YI",
        "Project Verticals",
        "Project Stakeholder",
        "YI Pillar",
        "SIG",
        "School",
        "Collage",
        "Social Link",
        "EC Member",
        "Member Name",
        "Impact",
        "Event Description"
        "Image",
    ]

    # Set the headers row
    sheet.append(headers)

    # Styling for headers (Bold and Centered)
    for cell in sheet[1]:
        cell.font = Font(bold=True)
        cell.alignment = Alignment(horizontal="center", vertical="center")

    # Get all event data
    event_data = Event_Data.objects.all()

    # Write event data rows
    for i in event_data:
        row = [
            i.date,
            i.your_name,
            i.event_name,
            i.event_venue,
            i.event_expense,
            i.role_yi,
            i.project_vertical,
            i.project_stakeholder,
            i.yi_pillar,
            i.which_SIG,
            i.school,
            i.collage,
            i.social_link,
            i.select_ec_member,
            i.event_member,
            i.total_impact,
            i.event_description
        ]
        sheet.append(row)
        # Now, for each event, if there are related images, we add them as hyperlinks.
        event_images = Event_Image.objects.filter(
            event=i
        )  # Access related Event_Image for each Event_Data
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
            image_link = ", ".join(img_urls)
            # Write the image links into the last column
            cell = f"R{sheet.max_row}"
            sheet[cell] = image_link
            # Make the cell contents a clickable link by adding the hyperlink to each image URL.
            sheet[cell].hyperlink = image_link
            sheet[cell].style = "Hyperlink"
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
        adjusted_width = max_length + 2
        sheet.column_dimensions[column].width = adjusted_width

    # Generate the response to download the file
    response = HttpResponse(
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    response["Content-Disposition"] = 'attachment; filename="Event_Data.xlsx"'
    workbook.save(response)
    return response


@login_required(login_url="index")
@never_cache
@cache_control(no_store=True, no_cache=True, must_revalidate=True, max_age=0)
def manager_list(request):
    # Check if the user has the 'Admin' role
    try:
        if request.user.yi_role not in ['Chapter Co-Chair', 'Chapter Chair', 'Admin']:
            return redirect("Error-Page")
    except Exception:
        return redirect(
            "Error-Page"
        )  # Redirect if the user doesn't have the Admin role

    # Make sure you're filtering by the 'user' field, not 'username'
    manager = LoginSide.objects.exclude(is_superuser=True)
    # Fetch all login roles (you can filter this as needed)
    login_role = Login_Role.objects.all()
    # Get the user's roles
    user_roles = request.user.login_role.all()
    sessions = Session.objects.filter(expire_date__gte=now())
    # Get user ids from the session data
    user_ids = [session.get_decoded().get("_auth_user_id") for session in sessions]
    # Query LoginSide objects for users
    active_users = LoginSide.objects.filter(id__in=user_ids)  # Get user objects
    active_user_names = [f"{user.first_name} {user.last_name}" for user in active_users]
    active_users_count = LoginSide.objects.filter(is_active=True).count()
    active_users_count = active_users.count()
    # Prepare context to pass to the template
    context = {
        "role": login_role,
        "managers": manager,
        "user_role": user_roles,
        "count": active_users_count,
        "name": active_user_names,
    }
    return render(request, "Admin/view_manager.html", context)


# Delete Ec  Member
@login_required(login_url="index")
def delete_member(request, member_id):
    if request.user.yi_role not in ['Chapter Co-Chair', 'Chapter Chair', 'Admin']:
            return redirect("Error-Page")

    try:

        if request.method == "POST":
            member = get_object_or_404(LoginSide, id=member_id)

            member.delete()
            messages.success(request, "Ec Member Deleted Succssfully")
        return redirect("View-manager")
    except Exception as e:

        messages.error(request, "Something Went Wrong Please  Try Again")
        return redirect("View-manager")
#Delete Multiple Event 

def delte_multiple(request):
    if request.method == 'POST':
        get_id = request.POST.getlist('delete_multiple')


# Delete Yi Event
@never_cache
@cache_control(no_store=True, no_cache=True, must_revalidate=True, max_age=0)
@login_required(login_url="index")
def delete_event(request, event_id):
    # Ensure only admins can delete events
    if request.user.yi_role not in ['Chapter Co-Chair', 'Chapter Chair', 'Admin']:
            return redirect("Error-Page")
    try:
        if request.method == "POST":
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
                    messages.error(request, "Error deleteing image")
                    img.delete()
            # Delete the Event_Data instance, which will also delete related Event_Image instances due to cascade
            event_to_delete.delete()
        # Redirect back to the Admin Dashboard after deletion
        return redirect("Admin_Dashboard")
    except Exception as e:
        messages.error(request, "Something Went Wrong Please  Try Again")


@login_required(login_url="index")
@never_cache
@cache_control(no_store=True, no_cache=True, must_revalidate=True, max_age=0)
def update_memeber(request, manager_id):
    if request.user.yi_role not in ['Chapter Co-Chair', 'Chapter Chair', 'Admin' ]:
            return redirect("Error-Page")
    update_manager_data = get_object_or_404(LoginSide, id=manager_id)
    try:
        if request.method == "POST":
            first_name = request.POST["manager_first_name"]
            last_name = request.POST["manager_last_name"]
            username = request.POST["manager_username"]
            yi_role = request.POST["yi_role"]
            email = request.POST["manager_email"]
            login_role = request.POST.getlist("login_role")
            phone_number = request.POST["manager_phone_number"]

        required_fields = {
            "First Name": first_name,
            "Last Name": last_name,
            "Username": username,
            "Yi Role": yi_role,
            # "EC Role": login_role,
            "Phone Number": phone_number,
        }

        for field, field_value in required_fields.items():
            if not field_value:
                messages.error(request, f"The {field} field is Required ")
                return redirect("View-manager")

        if request.method == "POST":
            update_manager_data.first_name = first_name
            update_manager_data.last_name = last_name
            update_manager_data.username = username
            update_manager_data.yi_role = yi_role
            update_manager_data.email = email
            login_roles = login_role
            update_manager_data.login_role.set(
                Login_Role.objects.filter(name__in=login_roles)
            )  # many to many filed change with set() in django

            # update_manager_data.password = request.POST['manager_password']
            update_manager_data.phone_number = phone_number
            print(update_manager_data.login_role)

            fields = [
                update_manager_data.first_name,
                update_manager_data.last_name,
                update_manager_data.yi_role,
                update_manager_data.email,
                update_manager_data.login_role,
                update_manager_data.phone_number,
            ]
            if any(field is None for field in fields):
                messages.error(request, "* Fields Are Required ")
                return redirect("View-manager")

            email_regex = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
            if not re.match(email_regex, update_manager_data.email):
                messages.error(request, "Enter Valid Email")
                return redirect("View-manager")

            if "manager_profile_img" in request.FILES:
                if (
                    update_manager_data.photo
                    and hasattr(update_manager_data.photo, "path")
                    and os.path.exists(update_manager_data.photo.path)
                ):
                    print(update_manager_data.photo.path)
                    os.remove(update_manager_data.photo.path)
                update_manager_data.photo = request.FILES["manager_profile_img"]

                if update_manager_data.photo:
                    try:
                        validator = FileExtensionValidator(
                            allowed_extensions=["jpeg", "jpg", "png"]
                        )
                        validator(update_manager_data.photo)
                    except ValidationError:
                        messages.error(
                            request,
                            "Invalid file type. Only .jpeg, .jpg, .png allowed.",
                        )
                        return redirect("View-manager")

                if update_manager_data.photo.size > 10 * 1024 * 1024:
                    messages.error(request, "Image size must be less than 10 MB")
                    return redirect("View-manager")

            try:

                update_manager_data.full_clean()
                update_manager_data.save()
                messages.success(request, "EC Member  Profile  Updated")

                return redirect("View-manager")
            except Exception as e:
                # print(e.message_dict.items())
                for field, errors in e.message_dict.items():

                    for error in errors:
                        messages.error(request, f"{field}: {error}")
                    return redirect("View-manager")

    except Exception:
        messages.error(request, "EC Member profile not Updated Please  Try Again")
        return redirect("View-manager")


@login_required(login_url="index")
@never_cache
@cache_control(no_store=True, no_cache=True, must_revalidate=True, max_age=0)
def update_event_data(request, event_id):
    if request.user.yi_role not in ['Chapter Co-Chair', 'Chapter Chair', 'Admin']:
            return redirect("Error-Page")
    else:
        try:
            update_event = get_object_or_404(Event_Data, id=event_id)

            if request.method == "POST":

                event_name = request.POST.get("event_name")
                project_vertical = request.POST.get("project_verticals")
                project_stakeholder = request.POST.get("project_stakeholder")
                yipiller = request.POST.get("yi_pillar")
                total_impact = request.POST.get("total_impact")
                event_date = request.POST.get("event_date")
                yirole = request.POST.get("role_yi")
                

            required_fields = {
                "Event Date": event_date,
                "Event Name": event_name,
                "Project Vertical": project_vertical,
                "Project Stakeholder": project_stakeholder,
                "Yi Piller": yipiller,
                "Yi Role": yirole,
                "Total Impact": total_impact,
            }
            for field, field_value in required_fields.items():
                if not field_value:
                    messages.error(request, f" The  {field} field is Required")
                    return redirect("Admin_Dashboard")

            if request.method == "POST":
                update_event.school = request.POST["school"]
                update_event.collage = request.POST["collage"]
                update_event.date = event_date
                update_event.event_name = event_name
                update_event.event_expense = request.POST["event_expense"]
                update_event.role_yi = yirole
                update_event.project_vertical = project_vertical
                update_event.project_stakeholder = project_stakeholder
                update_event.yi_pillar = yipiller
                update_event.social_link = request.POST["social_link"]
                update_event.event_member = request.POST["event_handle"]
                update_event.select_ec_member = request.POST['select_ec_member']
                update_event.total_impact = total_impact
                update_event.which_SIG = request.POST["sig_"]
                update_event.associate_partner = request.POST.get("associate_partners")
                event_image = request.FILES.getlist("event_image")
                update_event.event_description = request.POST["event_description"]
                
                for image in event_image: 
                    if image:
                        try:
                            validator = FileExtensionValidator(
                                allowed_extensions=["jpeg", "jpg", "png"]
                            )
                            validator(image)
                            
                            
                        except Exception as e:
                            messages.error(
                                request,
                                "Invalid file type. Only .jpeg, .jpg, .png allowed.",
                            )
                            return redirect("Admin_Dashboard")
                    Event_Image.objects.create(event=update_event, event_photo=image)
                update_event.save()
                messages.success(request, "Event Update Successfully")
                return redirect("Admin_Dashboard")
            else:
                messages.error(request, "Event not updated")
                return redirect("Admin_Dashboard")
        except Exception:
            messages.error(request, "Something Went Wrong Please  Try Again")
            return redirect("Admin_Dashboard")


@login_required(login_url="index")
@never_cache
@cache_control(no_store=True, no_cache=True, must_revalidate=True, max_age=0)
def event_image_delete(request, image_id):
    try:

        if request.method == "POST":
            image_to_delete = get_object_or_404(Event_Image, id=image_id)
            if image_to_delete.event_photo:
                image_to_delete.event_photo.delete()
                messages.success(request, "Image Delete")
            image_to_delete.delete()  # Delete the image record
    except Exception as e:
        messages.error(request, "Event Image not delete try again ")
    return redirect("Admin_Dashboard")


def members_diary(request):
    return render(request , 'Admin/members_diary.html')




def branding_dashboard(request):
    if request.user.yi_role not in ['Branding']:
        return redirect('Error-Page')
    
    
    
    
    total_event = Event_Data.objects.count()
    event_list = Event_Data.objects.all()
   
    total_impact_result = Event_Data.objects.aggregate(Sum("total_impact"))
    total_impact = (
        total_impact_result["total_impact__sum"]
        if total_impact_result["total_impact__sum"] is not None
        else 0
    )
    
    
    total_expense_result = Event_Data.objects.aggregate(Sum("event_expense"))
    total_expense = (
        total_expense_result["event_expense__sum"]
        if total_expense_result["event_expense__sum"] is not None
        else 0
    )
    
    member_name = (
        Event_Data.objects.all().values_list("your_name", flat=True).distinct()
    )
    
    vertical_name = (
        Event_Data.objects.all().values_list("project_vertical", flat=True).distinct()
    )
    total_vertical = vertical_name.count()
    
    stakeholder_name = (
        Event_Data.objects.all().values_list('project_stakeholder',flat=True).distinct()
    )
    
    
    yi_role_name = (
        Event_Data.objects.all().values_list('role_yi',flat=True).distinct()
    )
    
    yi_pillar_name = (
        Event_Data.objects.all().values_list("yi_pillar", flat=True).distinct()
    )
    
    
    event_date = (
        Event_Data.objects.all().values_list("date",flat=True).distinct()
    )

    def formatImpact(total_impact):
        s, *d = str(total_impact).partition(".")
        r = ",".join([s[x - 2 : x] for x in range(-3, -len(s), -2)][::-1] + [s[-3:]])
        return "".join([r] + d)
    
    def formatINR(total_expense):
        s, *d = str(total_expense).partition(".")
        r = ",".join([s[x - 2 : x] for x in range(-3, -len(s), -2)][::-1] + [s[-3:]])
        return "".join([r] + d)
    
    
    selected_vertical = request.GET.get("vertical", "all")
    if selected_vertical != "all":
        total_vertical = Event_Data.objects.filter(
            project_vertical=selected_vertical
        ).count()
        event_list = event_list.filter(project_vertical__icontains=selected_vertical)
        total_expense_result = event_list.aggregate(Sum("event_expense"))
        total_impact_result= event_list.aggregate(Sum("total_impact"))       
        total_impact = (total_impact_result["total_impact__sum"]if total_impact_result["total_impact__sum"] is not None
        else 0 )
        total_expense = (
            total_expense_result["event_expense__sum"]
            if total_expense_result["event_expense__sum"] is not None
            else 0
        )

    
    ec_name = request.GET.get("ec_name", "all")
    if ec_name and ec_name != "all":
        event_list = event_list.filter(your_name__icontains=ec_name)
        total_event = event_list.filter(your_name__icontains=ec_name).count
        total_impact_result= event_list.aggregate(Sum("total_impact"))       
        total_impact = (total_impact_result["total_impact__sum"]if total_impact_result["total_impact__sum"] is not None
        else 0 )
        total_expense_result = event_list.aggregate(Sum("event_expense"))
        total_expense = (
            total_expense_result["event_expense__sum"]
            if total_expense_result["event_expense__sum"] is not None
            else 0
        )
        
        
    yi_pillar = request.GET.get("yi_pillar")
    if yi_pillar and yi_pillar != "all":
        event_list = event_list.filter(yi_pillar__icontains=yi_pillar)
        total_event = event_list.filter(yi_pillar__icontains=yi_pillar).count()
        total_impact_result= event_list.aggregate(Sum("total_impact"))       
        total_impact = (total_impact_result["total_impact__sum"]if total_impact_result["total_impact__sum"] is not None
        else 0 )
        total_expense_result = event_list.aggregate(Sum("event_expense"))
        total_expense = (
            total_expense_result["event_expense__sum"]
            if total_expense_result["event_expense__sum"] is not None
            else 0
        )
    
    yi_role = request.GET.get("yi_role")
    if yi_role and yi_role != "all":
        event_list = event_list.filter(role_yi__icontains=yi_role)
        total_event = event_list.filter(role_yi__icontains=yi_role).count()
        total_impact_result= event_list.aggregate(Sum("total_impact"))       
        total_impact = (total_impact_result["total_impact__sum"]if total_impact_result["total_impact__sum"] is not None
        else 0 )
        total_expense_result = event_list.aggregate(Sum("event_expense"))
        total_expense = (
        total_expense_result["event_expense__sum"]
        if total_expense_result["event_expense__sum"] is not None
        else 0
    )
        
    stakeholder = request.GET.get("stakeholder")
    if stakeholder and stakeholder != "all":
        event_list = event_list.filter(project_stakeholder__icontains=stakeholder)
        total_event = event_list.filter(project_stakeholder__icontains=stakeholder).count()
        total_impact_result= event_list.aggregate(Sum("total_impact"))       
        total_impact = (total_impact_result["total_impact__sum"]if total_impact_result["total_impact__sum"] is not None
        else 0 )
        total_expense_result = event_list.aggregate(Sum("event_expense"))
        total_expense = (
            total_expense_result["event_expense__sum"]
            if total_expense_result["event_expense__sum"] is not None
            else 0
        )
        
        
    date = request.GET.get("event_date")
    if date and date != "all": 
        event_list = event_list.filter(date__icontains=date)
        total_event = event_list.filter(date__icontains=date).count()
        total_impact_result= event_list.aggregate(Sum("total_impact"))       
        total_impact = (total_impact_result["total_impact__sum"]if total_impact_result["total_impact__sum"] is not None
        else 0 )
        total_expense_result = event_list.aggregate(Sum("event_expense"))
        total_expense = (
            total_expense_result["event_expense__sum"]
            if total_expense_result["event_expense__sum"] is not None
            else 0
        )
    total_expense  = formatINR(total_expense)
    total_impact = formatImpact(total_impact)
    context = {
        'events':event_list,
        'total_event':total_event,
        'total_expense':total_expense,
        'total_impact':total_impact,
        'verticals':vertical_name ,
        'total_vertical':total_vertical,
        'stakeholder_name':stakeholder_name,
        'yi_role_name':yi_role_name,
        'yi_pillar_name':yi_pillar_name,
        'event_date': event_date,
        'member_name':member_name ,
    }
    
    return render(request,'Branding/dashboard.html',context)


def delete_multiple_event(request):
       
       if request.method == "POST":
        event_ids = request.POST.getlist('event_ids')  # Get selected checkboxes
        if event_ids:
            Event_Data.objects.filter(id__in=event_ids).delete()
        return redirect('Admin_Dashboard')

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
            event = Event_Data.request.query_params.get("id")
            event.delete()  # Delete the object
            return Response(
                {"message": "Event deleted successfully"},
                status=status.HTTP_204_NO_CONTENT,
            )
        except Event_Data.DoesNotExist:
            return Response(
                {"error": "Event not found"}, status=status.HTTP_404_NOT_FOUND
            )

    def put(self, request):
        # Get the event instance based on the provided ID
        event = Event_Data.objects.get(pk=request.data.get("id"))
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
    event_data = Event_Data.objects.all().values_list("your_name", flat=True).distinct()
    # event_impact = Event_Data.objects.all().values_list('total_impact',flat=True).annotate(Sum('total_impact'))
    event_impact_by_name = (
        Event_Data.objects.values("your_name")
        .annotate(total_impact=Sum("total_impact"))
        .order_by("your_name")
    )

    project_verticals = (
        Event_Data.objects.all().values_list("project_vertical", flat=True).distinct()
    )
    # event_impact = Event_Data.objects.all().values_list('total_impact',flat=True).annotate(Sum('total_impact'))
    project_verticals_by_name = (
        Event_Data.objects.values("your_name")
        .annotate(total_impact=Sum("project_vertical"))
        .order_by("project_vertical")
    )

    context = {
        "name": event_data,
        "impact_data": event_impact_by_name,
        "verticals": project_verticals,
    }
    return render(request, "Admin/chart/admin_chart.html", context)





# ForgotPasssword Side
class CustomPasswordResetView(PasswordResetView):
    template_name = "password/password_reset_form.html"
    email_template_name = "password/password_reset_email.html"
    success_url = reverse_lazy("password_reset_done")


class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = "password/password_reset_done.html"


class CustomPasswordResetConfirm(PasswordResetConfirmView):
    template_name = "password/password_reset_confirm.html"
    success_url = reverse_lazy("password_reset_complete")


def password_update_done(request):
    return render(request, "Admin/components/password_update_done.html")


# Utility functions
# def get_active_users():
#     """Get active users from current sessions."""
#     sessions = Session.objects.filter(expire_date__gte=now())
#     user_ids = []
#     for session in sessions:
#         data = session.get_decoded()
#         user_id = data.get('_auth_user_id')
#         if user_id:
#             user_ids.append(user_id)

#     active_users = LoginSide.objects.filter(id__in=user_ids)
#     active_user_names = [f"{user.first_name} {user.last_name}" for user in active_users]
#     active_users_count = active_users.count()

#     return {
#         'name': active_user_names,
#         'count': active_users_count
#     }

# def admin_required(view_func):
#     """Decorator to check if user has admin role."""
#     def wrapper(request, *args, **kwargs):
#         if not request.user.is_authenticated:
#             return redirect('index')
#         if not request.user.login_role.filter(name='Admin').exists():
#             return redirect('Error-Page')
#         return view_func(request, *args, **kwargs)
#     return wrapper

# import csv
# import requests # type: ignore
# from io import StringIO
# from django.shortcuts import render

# def live_google_form_data(request):
#     csv_url = 'https://docs.google.com/spreadsheets/d/1WuoI9-47TGfBPdWqpnHQ2fZ3-sYw7Eh2JSADy-HAkXs/export?format=csv'
#     data = []

#     response = requests.get(csv_url)
#     if response.status_code == 200:
#         csv_file = StringIO(response.text)
#         reader = csv.DictReader(csv_file)
#         for row in reader:
#             data.append(row)

#     return render(request, 'Admin/google_live_data.html', {'data': data})










