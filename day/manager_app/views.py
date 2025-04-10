from io import BytesIO
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import login,authenticate,logout,update_session_auth_hash
from admin_app.models import LoginSide,Login_Role
from matplotlib import pyplot as plt
import matplotlib
import numpy as np
from .models import Event_Data,Event_Image
from  django.contrib.auth.decorators import login_required
from django.db.models import Avg, Sum
import os
from django.core.validators import FileExtensionValidator 
# Create your views here.


# def manager_login(request):
#     if request.method == 'POST':
#         username = request.POST.get('manager_username')
#         password = request.POST.get('manager_password')

#         manager_user = authenticate(request,username=username,password=password)
#         if manager_user is not None:
#             if manager_user.login_role.filter(name='Manager').exists():
#                 login(request,manager_user)
#                 return redirect('manager-dashboard')
#             else:
#                 messages.error(request,"Incorrect Username Password")
#         else:
#             messages.error(request, "Invalid Username or Password")
#             return redirect('index')


#     return render(request,'index.html')



# @login_required(login_url='index')
# def manager_signup(request):
#     if request.method == "POST":
#         manager_username = request.POST.get('manager_username')
#         first_name = request.POST.get('first_name')
#         last_name = request.POST.get('last_name')
#         password = request.POST.get('password1')
#         phone = request.POST.get('add_phone')
#         profile_img = request.FILES.get('profile_img')
#         confirm_password = request.POST.get('password2')
#         manager_email = request.POST.get('manager_email')
#         # which_role = request.POST.getlist('which_role')





#         if len(phone) != 10 or not phone.isdigit():
#             messages.error(request, "Phone number must be 10 digits.")
#             return render(request,'manager/manager_signup.html')

#         if len(password) < 8 or not any(c.isupper() for c in password) or not any(
#                 c in "!@#$%^&*()_+-={}[]|\\:;\"'<>,.?/~`" for c in password):
#             messages.error(request,"Password must be at least 8 characters with one uppercase letter and one special character")
#             return render(request, 'manager/manager_signup.html')

#         if password != confirm_password:
#             messages.error(request, "Password and Confirm Password must be Same")
#             return render(request,'manager/manager_signup.html')


#         manager_user = LoginSide.objects.create_user(username=manager_username,
#                                                      first_name=first_name,
#                                                      last_name=last_name,
#                                                      photo=profile_img,
#                                                      password=password,
#                                                      email=manager_email,
#                                                      phone_number=phone,
#                                                      login_role='Manager',)
#         manager_user.save()
#         messages.success(request, 'New Manager Created')
#         return redirect('manager-signup')
#     return render(request,'manager/manager_signup.html')


@login_required(login_url='index')
def manager_logout(request):
    logout(request)
    request.session.clear()
    return redirect('index')

@login_required(login_url='index')
def about_yi(request):
    return render(request,'components/AboutYi.html')

@login_required(login_url='index')
def manager_update(request,manager_id):
    if  request.user.yi_role == 'Chapter Co-Chair' or  request.user.yi_role == 'Chapter Chair':
        return redirect('Error-Page')
    
    try:
        if request.method == 'POST':
            first_name = request.POST['manager_first_name']
            last_name = request.POST['manager_last_name']
            username = request.POST['username']
            # yi_role = request.POST['yi_role']
            email = request.POST['manager_email']
            # login_role = request.POST.getlist('login_role')
            phone_number = request.POST['phone_number']
            
        required_fields = {
                'First Name': first_name,
                'Last Name' :  last_name,
                'Username' :username,
                'Email':email,
                'Phone Number':phone_number,
            }
        for field,field_value in required_fields.items():
            if not field_value:
                messages.error(request,f"The {field} field is Required ")
                return redirect('manager-profile')
        
        if request.method == 'POST':
            manager_profile = get_object_or_404(LoginSide, id=manager_id)
            manager_profile.first_name = first_name
            manager_profile.last_name = last_name
            manager_profile.email = email
            manager_profile.username = username
            manager_profile.phone_number = phone_number
            
            if 'manager_profile_img' in request.FILES:
    
                if manager_profile.photo and hasattr(manager_profile.photo, 'path') and os.path.exists(manager_profile.photo.path):
                    print(manager_profile.photo.path)
                    os.remove(manager_profile.photo.path)
                    manager_profile.photo.path.delete()
                manager_profile.photo = request.FILES['manager_profile_img']
                
                if manager_profile.photo.size > 4*1024*1024:
                    messages.error(request,'Image Size must be 4mb')
                    return redirect('manager-profile')
            try:      
                manager_profile.save()
                messages.success(request,'Profile Updated')
                return redirect('manager-profile')
            except Exception as e:
                for field,errors in e.message_dict.items():
                    for error in errors:
                        messages.error(request,f"{error} ")
                    return redirect('manager-profile')
    except Exception as e:
        messages.error(request, f'Error updating profile: {str(e)}')
        return redirect('manager-profile')


@login_required(login_url='index')
def manager_password(request):
    if  request.user.yi_role == 'Chapter Co-Chair' or  request.user.yi_role == 'Chapter Chair':
        return redirect('Error-Page')
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

@login_required(login_url='index')
def manager_dashboard(request):
    if  request.user.yi_role == 'Chapter Co-Chair' or  request.user.yi_role == 'Chapter Chair':
        return redirect('Error-Page')
 
    user_roles = request.session.get('userrole', [])
    
    # ec_member = LoginSide.objects.all().values_list('first_name', flat=True).distinct().exclude(is_superuser=True)
    ec_member = LoginSide.objects.all().distinct().exclude(is_superuser=True)
    ec_member_names = [f"{member.first_name} {member.last_name}"for member in ec_member]
    if user_roles:
        context = {
            'role': user_roles,
            'ec_member':ec_member_names ,# Pass the role to the template
        }
    else:
        context = {
            'role': 'Unknown',
            'ec_member':ec_member_names ,
        }
    
    return render(request,'member/add_event.html',context)

@login_required(login_url='index')
def manager_profile(request):
    if  request.user.yi_role == 'Chapter Co-Chair' or  request.user.yi_role == 'Chapter Chair':
        return redirect('Error-Page')

    return render(request,'member/member_profile.html')

@login_required(login_url='index')
def event_list(request):

    user = request.user
    all_event = Event_Data.objects.filter(user=user)

    context = {
        'user': user,
        'k1': all_event
    }
    return render(request, 'member/event_list.html', context)


def delete_event_data(request,events_id):
    try:
        if request.method == 'POST':
            delete_events = get_object_or_404(Event_Data,id=events_id)
            event_img  = delete_events.event_photo.all()
            
            for img in event_img:
                try:
                    path = img .event_photo.path
                    print(path)
                    if os.path.isfile(path):
                        os.remove(path)
                except Exception as e:
                    messages.error(request,'Error deleteing image')
                    img.delete()
            
            delete_events.delete()
            
            return redirect('member-dashbaord')
    except Exception as e:
        messages.error(request,'Something went Wrong plz Try Again Event was not Deleted ')

    return render (request,'member/dashboard.html')



def update_event_data(request,update_id):

    if  request.user.yi_role == 'Chapter Co-Chair' or  request.user.yi_role == 'Chapter Chair':
        return redirect('Error-Page')
    
    try:
        if request.method == 'POST':
            update_event = get_object_or_404(Event_Data,id = update_id)
            
            if request.method == 'POST':
            
                event_name = request.POST.get('event_name')
                project_vertical = request.POST.get('project_verticals')
                project_stakeholder = request.POST.get('project_stakeholder')
                yipiller = request.POST.get('yi_pillar')
                total_impact = request.POST.get('total_impact')
                event_date = request.POST.get('event_date')
                yirole  = request.POST.get('role_yi')
                
            required_fields = {
                    'Event Date': event_date,
                    'Event Name': event_name,
                    'Project Vertical': project_vertical,
                    'Project Stakeholder': project_stakeholder,
                    'Yi Piller': yipiller,
                    'Yi Role': yirole,
                    'Total Impact': total_impact,}
                
            for field ,field_value in required_fields.items():
                if not field_value:
                    messages.error(request,f" The  {field} field is Required")
                    return redirect('member-dashbaord') 
            
            update_event.event_name = event_name 
            update_event.collage =  request.POST['collage']
            update_event.school = request.POST['school']
            update_event.date = event_date
            update_event.role_yi = yirole
            update_event.project_vertical = project_vertical
            update_event.project_stakeholder = project_stakeholder
            update_event.yi_pillar = yipiller
            update_event.social_link = request.POST['social_link']
            update_event.event_member = request.POST['event_member']
            update_event.select_ec_member = request.POST['select_ec_member']
            update_event.event_description = request.POST["event_description"]
            update_event.total_impact = total_impact
            update_event.which_SIG  = request.POST['sig_']
            update_event.associate_partner = request.POST.get('associate_partners')
            event_image = request.FILES.getlist('event_image')
            for image in event_image:
                if image:
                        try:
                            validator = FileExtensionValidator(
                                allowed_extensions=["jpeg", "jpg", "png"]
                            )
                            validator(image)
                            if len(event_image) > 6 and event_image:  # event_images is a list of image files
                                messages.error(request, "You can Upload only 6 Images")
                                return redirect('manager-dashboard')
                        except Exception as e:
                            messages.error(
                                request,
                                "Invalid file type. Only .jpeg, .jpg, .png allowed.",
                            )
                            return redirect('member-dashbaord')
                Event_Image.objects.create(event=update_event,event_photo = image)
            update_event.save()
            
            
            messages.success(request,'Event updated succssfully')
            return redirect('member-dashbaord')
        else:
            messages.error(request,'Data not update')
            return redirect('member-dashbaord')
            
    except Exception as e:
        
        messages.error(request,'Data not update')
        return redirect('member-dashbaord')
    return render (request,'member/dashboard.html')


def delete_event_image(request,image_id):
    try:
   
        if request.method == 'POST':
            image_to_delete = get_object_or_404(Event_Image,id = image_id )
            if image_to_delete.event_photo:
                image_to_delete.event_photo.delete()
            image_to_delete.event_photo.delete()
        return redirect('member-dashbaord')
    except Exception as e:
        messages.error(request,'image not deleted ')
        return render(request, 'member/dashboard.html')
        
            
    # return render(request, 'member/event_list.html')




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

from django.http import JsonResponse
@login_required(login_url='index')
def event_data(request):
    if  request.user.yi_role == 'Chapter Co-Chair' or  request.user.yi_role == 'Chapter Chair':
        return redirect('Error-Page')
    
    
    try:
        
        
        if request.method == 'POST':
            your_name = request.POST.get('your_name', '')
            event_date = request.POST.get('event_date', '')
            role_yi = request.POST.get('role_yi', '')
            sig_option = request.POST.get('sig_', '')
            event_member = request.POST.get('handel_by', '')
            select_ec_member = request.POST.get('select_member', '')
            project_verticals = request.POST.get('project_verticals', '')
            project_stakeholder = request.POST.get('project_stakeholder', '')
            yi_pillar = request.POST.get('yi_pillar', '')
            social_link = request.POST.get('social_link', '')
            total_impact = request.POST.get('total_impact', '')
            event_expense = request.POST.get('event_expense', '')
            event_venue = request.POST.get('event_venue', '')
            event_name = request.POST.get('event_name', '')
            event_description = request.POST.get('event_description', '')
            school = request.POST.get('school', '')
            collage = request.POST.get('collage', '')
            associate_partner = request.POST.get('associate_partner', '')
            
            if event_expense ==  '':
                event_expense = 0

          
          

            required_fields = {
                        'Event Date': event_date,
                        'Project Vertical': project_verticals,
                        'Project Stakeholder': project_stakeholder,
                        'Yi Piller':  yi_pillar,
                        'Yi Role':  role_yi,
                        'Total Impact': total_impact,
            }
            
            
            for field ,field_value in required_fields.items():
                if not field_value:
                    messages.error(request,f" The  {field} field is Required")
                    return redirect('manager-dashboard') 

            event_image = request.FILES.getlist('event_img')

            # if len(event_image) > 6 and event_image:  # event_images is a list of image files
            #     messages.error(request, "You can Upload only 6 Images")
            #     return redirect('manager-dashboard')
        

       
            for img in event_image:
                try:
                    validator = FileExtensionValidator(allowed_extensions=['jpeg','jpg','png'])
                    validator(img)
                except Exception:
                    messages.error(request,"Invalid file type  Only .jpg , jpeg , and .png")
                    return redirect('manager-dashboard')
                

            EventData = Event_Data.objects.create(
                your_name=your_name,
                date=event_date,
                role_yi=role_yi,
                event_member=event_member,
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
                select_ec_member=select_ec_member,
                event_description=event_description,
                # event_photo=event_images,
                associate_partner=associate_partner,
                user=request.user
            )

            for image in event_image:
                Event_Image.objects.create(event_photo=image,event=EventData)
            messages.success(request, 'Thank you for insert data')
            return redirect('member-dashbaord')
            
                # return JsonResponse({'status':'Data inserted'})
           
    except Exception as e:
        messages.error(request, f"Something went wrong: {str(e)}")
        return redirect('manager-dashboard')
        
            
    return render(request, 'member/add_event.html')





def dashboard(request):
    if  request.user.yi_role == 'Chapter Co-Chair' or  request.user.yi_role == 'Chapter Chair':
        return redirect("Error-Page")
    user = request.user
    all_event = Event_Data.objects.filter(user=user)
    total_event = Event_Data.objects.filter(user=user).count()
    total_impact_data =  Event_Data.objects.filter(user=user).aggregate(Sum('total_impact'))
    total_impact = total_impact_data['total_impact__sum'] if total_impact_data['total_impact__sum']is not None else 0
    user_roles = request.session.get('userrole', [])
    image = request.session.get('image', None)
    ec_member = LoginSide.objects.all().distinct().exclude(is_superuser=True)
    ec_member_names = [f"{member.first_name} {member.last_name}"for member in ec_member]
    # event_name = Event_Data.objects.filter(user=user).values_list('project_vertical',flat=True).distinct()
    # event_impact = Event_Data.objects.filter(user=user).values('project_vertical').annotate(total_impact=Sum('total_impact'))
    
    # event_impact = Event_Data.objects.filter(user=user).values('project_vertical').annotate(total_impact=Sum('total_impact'))
    # Map event names to their corresponding total impact
    # event_total_dict = {item['project_vertical']: item['total_impact'] for item in total_event}

    # Adjust event_impact to reflect the correct order of event_name
    # aligned_event_impact = [event_total_dict.get(event, 0) for event in event_name]
    
    
    def formatImpact(total_impact):
        s, *d = str(total_impact).partition(".")
        r = ",".join([s[x-2:x] for x in range(-3, -len(s), -2)][::-1] + [s[-3:]])
        return "".join([r] + d)
    
    
    total_impact = formatImpact(total_impact)
   
    
    
        
              # Pass the role to the template
       
    user = request.user
    all_event = Event_Data.objects.filter(user=user)
    # print(event_name)
    # print(event_impact)

    context = {  'total_event':total_event,
                 'total_impact':total_impact,
                #  'event_name': event_name,
                #  'impact':aligned_event_impact,
                    'events': all_event,
                    'role':user_roles,
                    'image':image,
                    'ec_member ':ec_member_names                   
                    
                }

    return render(request,'member/dashboard.html',context)




# Masoom Side

# def masoom_dashboard(request):
#     return render(request,'Masoom/masoom_dashboard.html')



# def update_event_data(request, event_id):
#     if not request.user.login_role.filter(name='Admin').exists():
#         return redirect('Error-Page')
#     else:
#         # Fetch the event object that you want to update
#         update_event = get_object_or_404(Event_Data, id=event_id)

#         # Fetch the Event_Image instances related to this event
#         event_images = Event_Image.objects.filter(event=update_event)

#         if request.method == 'POST':
#             # Update Event_Data fields
#             update_event.school = request.POST['school']
#             update_event.collage = request.POST['collage']
#             update_event.date = request.POST['event_date']
#             update_event.event_name = request.POST['event_name']
#             update_event.event_expense = request.POST['event_expense']
#             update_event.role_yi = request.POST['role_yi']
#             update_event.project_vertical = request.POST['project_verticals']
#             update_event.project_stakeholder = request.POST['project_stakeholder']
#             update_event.yi_pillar = request.POST['yi_pillar']
#             update_event.social_link = request.POST['social_link']
#             update_event.event_handle = request.POST['event_handle']
#             update_event.total_impact = request.POST['total_impact']
#             update_event.which_SIG = request.POST['sig_']
#             update_event.associate_partner = request.POST.get('associate_partners')

#             # Handle image uploads: if new images are uploaded, create or update Event_Image instances
#             if 'event_image' in request.FILES:
#                 # For each uploaded file, create a new Event_Image entry
#                 uploaded_images = request.FILES.getlist('event_image')

#                 for uploaded_image in uploaded_images:
#                     Event_Image.objects.create(event=update_event, event_photo=uploaded_image)
#                 # Alternatively, you could update existing images if necessary
#                 # for image in event_images:
#                 #     image.event_photo = updated_image_file
#                 #     image.save()

#             # Save the Event_Data object
#             update_event.save()

#             # Show a success message
#             messages.success(request, 'Event Updated Successfully')
#             return redirect('Admin_Dashboard', event_id=update_event.i.)

#         else:
#             # If the method is not POST, show an error message
#             messages.error(request, 'Event not updated')
#             return redirect('Admin_Dashboard')



