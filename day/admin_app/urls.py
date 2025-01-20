from django.conf import settings
from django.urls import path
from .views import *
from django.conf.urls.static import static

urlpatterns = [
    path('Admin-Login',Admin_Login,name='Admin_Login'),
    path('Admin-Signup',Admin_Signup,name='Admin_Signup'),
    path('Admin-Dashboard',Admin_Dashboard,name='Admin_Dashboard'),
    path('Admin-Profile',Admin_Profile,name='Admin_Profile'),
    path('Admin-Update/<int:admin_id>/',Admin_update,name='Admin_Update'),
    path('Admin-Password',admin_password,name='Admin_Password'),
    path('Admin-Logout',admin_logout,name='Admin_Logout'),
    path('Event-List',Event_list,name='Event_List'),
    path('View-manager',manager_list,name='View-manager'),
    path('download_excel',download_excel,name='download_excel'),
    path('Error',error_page,name='Error-Page'),
    path('delete-data',delete_multiple,name='delete_multiple'),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)