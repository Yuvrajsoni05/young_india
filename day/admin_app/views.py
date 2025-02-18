from collections import Counter
from io import BytesIO
# from openpyxl.drawing.image import Image
from django.core.paginator import Paginator
import matplotlib
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
import csv
from django.http import HttpResponse
import openpyxl
from .serializer import EventDataSerializer
from manager_app.models import Event_Data,Event_Image
from django.contrib import messages
from django.utils.decorators import method_decorator

from django.shortcuts import render

from django.views.decorators.cache import never_cache
# Create your views here.







def index(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        login_roles = request.POST.get('login_roles')  # Selected role from form input

        # Authenticate the user
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # Ensure user is a LoginSide instance (if using a custom user model)
            if isinstance(user, LoginSide):
                # Get the selected role from the database
                selected_role = Login_Role.objects.filter(name=login_roles).first()

                if selected_role and selected_role in user.login_role.all():  # Check if user has the selected role
                    login(request, user)

                    # Store the role in the session so that it can be accessed across requests
                    request.session['user_roles'] = selected_role.name

                    # Redirect based on role
                    if selected_role.name == 'Admin':  # If user has Admin role
                        return redirect('Admin_Dashboard')
                    else:
                        return redirect('manager-dashboard')
                else:
                    # Role doesn't match, redirect back to the login page
                    return redirect('index')
            else:
                # In case of an invalid user instance
                return redirect('index')
        else:
            # If authentication fails, redirect to login page
            return redirect('index')

    # Get all roles to pass to the form
    roles = Login_Role.objects.all()
    context = {
        'roles': roles
    }
    return render(request, 'index.html', context)







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




from django.http import JsonResponse

def get_username(request):
    user  = request.user
    data = {
        "username": "Yuvraj Soni" # You can customize this with any name
    }
    return JsonResponse(data)




@login_required(login_url='index')
def Admin_Signup(request):
    if not request.user.login_role.filter(name='Admin').exists():
        return redirect('Error-Page')

    if request.method == 'POST':
        username = request.POST.get('add_username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        password = request.POST.get('password1')
        profile_img = request.FILES.get('profile_img')
        confirm_password = request.POST.get('password2')
        Admin_email = request.POST.get('add_email')
        phone = request.POST.get('add_phone')
        login_role = request.POST.getlist('login_role')  # Use getlist to fetch multiple roles



        if profile_img.size > 4*1024*1024:
            messages.error(request,'Image Size must be 4mb')
            return redirect('Admin_Signup')

        if LoginSide.objects.filter(email=Admin_email).exists():
            messages.error(request, "This email is already taken.")
            return redirect('Admin_Signup')

        if LoginSide.objects.filter(username=username).exists():
            messages.error(request, "This Username is already taken.")
            return redirect('Admin_Signup')

        # Validation checks
        if len(phone) != 10 or not phone.isdigit():
            messages.error(request, "Phone number must be 10 digits.")
            return redirect('Admin_Signup')

        if len(password) < 8 or not any(c.isupper() for c in password) or not any(
                c in "!@#$%^&*()_+-={}[]|\\:;\"'<>,.?/~`" for c in password):
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
            phone_number=phone
        )

        # Assign selected roles to the user
        roles = Login_Role.objects.filter(name__in=login_role)  # Filter roles based on selected ones
        Admin_User.login_role.set(roles)  # Assign multiple roles
        Admin_User.save()

        messages.success(request, "Admin Created")

        return redirect('Admin_Dashboard')

    # Fetch all roles for the dropdown
    login_role = Login_Role.objects.all()
    context = {
        'role': login_role
    }

    return render(request, 'Admin/AdminSignup.html', context)


# if request.user.login_role != 'Admin':
    #     return redirect('Error-Page')
    # else:


@login_required(login_url='index')
def Admin_Profile(request):
    if not request.user.login_role.filter(name='Admin').exists():
        return redirect('Error-Page')
    # else:
    #     return redirect('Admin_Profile')
    return render(request, 'Admin/Admin_Profile.html')


@login_required(login_url='index')
def Admin_update(request,admin_id):
    if not request.user.login_role.filter(name='Admin').exists():
        return redirect('Error-Page')
    else:
        if request.user.login_role.filter(name='Admin').exists():
            if request.method == 'POST':
                admin_profile = get_object_or_404(LoginSide,id=admin_id)
                admin_profile.first_name = request.POST['admin_firstname']
                admin_profile.last_name = request.POST['admin_lastname']
                admin_profile.email = request.POST['admin_email']

                admin_profile.username = request.POST['admin_username']
                admin_profile.phone_number = request.POST['admin_phone']
                if 'admin_profile_img' in request.FILES:
                    admin_profile.photo = request.FILES['admin_profile_img']
                admin_profile.save()
                messages.success(request,'Profile Updated')
                return redirect('Admin_Profile')
            else:
                messages.error(request,'Profile not Updated')
    # return render(request,'Admin/Admin_Profile.html')


@login_required(login_url='index')
def admin_password(request):
    if request.user.login_role.filter(name='Admin').exists():
        if request.method == 'POST':
            old_password = request.POST.get('old_password')
            new_password = request.POST.get('new_password')
            confirm_password = request.POST.get('confirm_password')
            admin_user =request.user
            if not admin_user.check_password(old_password):
                messages.error(request, "Old Password Incorrect")
                return redirect('Admin_Profile')

            if len(new_password) < 8 or not any(c.isupper() for c in   new_password) or not any(
                    c in "!@#$%^&*()_+-={}[]|\\:;\"'<>,.?/~`" for c in new_password):
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


@login_required(login_url='index')
def admin_logout(request):
    logout(request)
    request.session.clear()
    return redirect('index')


@login_required(login_url='index')
def Admin_Dashboard(request):
    if not request.user.login_role.filter(name='Admin').exists():
        return redirect('Error-Page')
    total_event = Event_Data.objects.count()
    total_user_data = LoginSide.objects.filter(login_role='Manager')
    total_user = total_user_data.count()


    total_expense_result = Event_Data.objects.aggregate(Sum('event_expense'))
    total_expense =total_expense_result['event_expense__sum'] if total_expense_result['event_expense__sum'] is not None else 0


    total_impact_result = Event_Data.objects.aggregate(Sum('total_impact'))
    total_impact = total_impact_result['total_impact__sum'] if total_impact_result['total_impact__sum']is not None else 0
    impact_avg = Event_Data.objects.aggregate(Avg('total_impact'))
    avg_impact = impact_avg['total_impact__avg'] if impact_avg['total_impact__avg']is not None else 0


    all_user = LoginSide.objects.all().distinct()
    login_role = Login_Role.objects.all()



    manager_role = Event_Data.objects.all().values_list('project_verticals',flat=True).distinct()
    manager_name = Event_Data.objects.all().values_list('your_name', flat=True).distinct()

    login_role = request.GET.get('login_role')

    if login_role and login_role != 'login_role':
        event_role = Event_Data.objects.filter(login_role=login_role)
    else:
        event_role= Event_Data.objects.filter(login_role=login_role)
        


    search = request.GET.get('search')
    if search and search != 'all':
        event_list = Event_Data.objects.filter(your_name=search)
    
    else:
        event_list = Event_Data.objects.all()

    events_list = Event_Data.objects.all()
    paginator = Paginator(events_list, 10)  # Show 10 events per page
    page_number = request.GET.get('page')
    events = paginator.get_page(page_number)
    contex = {
        'users_data':all_user,
        'role':login_role,
        'total_manager' :total_user,
        'total_event':total_event,
        'total_impact':total_impact,
        'impact_avg':avg_impact,
        'total_expense':total_expense,
        'events':event_list,
         'm1': manager_name,
    }
    return render(request, 'Admin/AdminDashboard.html',contex)


@login_required(login_url='index')
def Event_list(request):
    if not  request.user.login_role.filter(name='Admin').exists():
        return redirect('Error-Page')
    manager_name = Event_Data.objects.all().values_list('your_name', flat=True).distinct()
  #  project_verticals = Event_Data.objects.all().values_list('project_vertical',flat=True).distinct()






    search = request.GET.get('search')
    if search and search != 'all':
        event_list = Event_Data.objects.filter(your_name=search)
    else:
        event_list = Event_Data.objects.all()
    context = {
        'events': event_list,
        'm1': manager_name,

    }
    return render(request, 'Admin/event_list.html', context)

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

def error_page(request ):
    return render(request,'Admin/components/Error_404.html',)

from openpyxl.styles import Font
from openpyxl.drawing.image import Image
import openpyxl
from openpyxl.drawing.image import Image
from django.http import HttpResponse

from io import BytesIO
from PIL import Image as PILImage
from openpyxl.drawing.image import Image
import os
from django.conf import settings

def download_excel(request):
    workbook = openpyxl.Workbook()
    sheet = workbook.active
    sheet.title = 'Event Data'

    headers = [
        'Event Date', 'Manager Name', 'Event Name', 'Event Venue', 'Event Expense', 'Role YI', 'Project Verticals',
        'Project Stakeholder', 'YI Pillar', 'SIG', 'School', 'Collage', 'Associate Partner', 'Event Handle', 'Impact', 'Image'
    ]

    # Set the headers in the first row
    sheet.append(headers)

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

        # Now, for each event, if there are related images, we add them.
        event_images = i.event_photo.all()  # Access related Event_Image for each Event_Data

        # Check if there are images for this event
        for img in event_images:
            if img.event_photo:
                img_path = os.path.join(settings.MEDIA_ROOT, img.event_photo.name)

                # Open the image with Pillow
                try:
                    pil_img = PILImage.open(img_path)

                    # Save the image to a BytesIO stream
                    img_stream = BytesIO()
                    pil_img.save(img_stream, format='PNG')
                    img_stream.seek(0)

                    # Create an Image object for openpyxl from the BytesIO stream
                    openpyxl_img = Image(img_stream)
                    openpyxl_img.width = 80
                    openpyxl_img.height = 30

                    # Insert the image in the corresponding row
                    img.anchor = f'O{sheet.max_row}'  # The 'O' column is the 15th column (Image column)
                    sheet.add_image(openpyxl_img)
                except Exception as e:
                    print(f"Error inserting image: {e}")
                    continue

    # Generate the response to download the file
    response = HttpResponse(
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    response['Content-Disposition'] = 'attachment; filename="Event_Data.xlsx"'

    workbook.save(response)
    return response


def manager_list(request):
    if not request.user.login_role.filter(name='Admin').exists():
        return redirect('Error-Page')
    manager = LoginSide.objects.all().distinct()
    # login_role = Login_Role.objects.exclude(is_superuser=False)
    login_role = Login_Role.objects.exclude(name = 'superuser')
    # login_role = Login_Role.objects.exclude(name='superuser')  # Example if you have a role field

    contex = {
        'role' :login_role,
        'managers' :manager
    }
    return render(request,'Admin/view_manager.html',contex)


def delete_handler(request,handler_id):
    if not request.user.login_role.filter(name='Admin').exists():
        return redirect('Error-Page')
    if request.method == 'POST':
        handler = get_object_or_404(LoginSide, id=handler_id)
        handler.delete()
    return redirect('View-manager')





def delete_event(request,event_id):
    if not request.user.login_role.filter(name='Admin').exists():
        return redirect('Error-Page')
    if request.method == 'POST':
        delete_events = get_object_or_404(Event_Data,id=event_id)
        delete_events.delete()
    return redirect('Event_List')


def update_manager(request,manager_id):
    if not request.user.login_role.filter(name='Admin').exists():
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

        if update_manager_data.photo.size > 4*1024*1024:
            messages.error(request,'Image Size must be 4mb ')
            return redirect('View-manager')
        update_manager_data.save()
        messages.success(request, 'Manager profile  Updated')

    else:
        messages.error(request,'Manager profile not Updated')
    return redirect('View-manager')



def update_event_data(request,event_id):
    if not request.user.login_role.filter(name='Admin').exists():
        return redirect('Error-Page')
    else:
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
                update_event.save()
                messages.success(request,'Event Updated')
                return redirect('Admin_Dashboard')

            else:
                messages.error(request,'Event not updated')
                return redirect('Admin_Dashboard')



@method_decorator(login_required(login_url='index'),name='get')
class EventDataAPI(APIView):
    def get(self,request):
        event = Event_Data.objects.all()
        serializers = EventDataSerializer(event,many=True)
        return Response(serializers.data)



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

def admin_chart(request):
    event_data = Event_Data.objects.all().values_list('your_name', flat=True).distinct()
    # event_impact = Event_Data.objects.all().values_list('total_impact',flat=True).annotate(Sum('total_impact'))
    event_impact_by_name = Event_Data.objects.values('your_name').annotate(total_impact=Sum('total_impact')).order_by('your_name')
    context = {
        'name': event_data,
        'impact_data':event_impact_by_name

    }
    return render(request, 'Admin/chart/admin_chart.html', context)


# Password Side
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView
from django.urls import reverse_lazy


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








































