from tkinter.font import names

from django.conf import settings
from django.urls import path
from .views import *
from django.conf.urls.static import static

from .views import EventDataAPI

urlpatterns = [
    path('',index,name='index'),
    path('Admin-Login',Admin_Login,name='Admin_Login'),
    path('Admin-Signup',Admin_Signup,name='Admin_Signup'),
    path('Admin-Dashboard',Admin_Dashboard,name='Admin_Dashboard'),
    path('Admin-Profile',Admin_Profile,name='Admin_Profile'),
    path('Admin-Update/<uuid:admin_id>/',Admin_update,name='Admin_Update'),
    path('Admin-Password',admin_password,name='Admin_Password'),
    path('Admin-Logout',admin_logout,name='Admin_Logout'),
    path('Event-List',Event_list,name='Event_List'),
    path('View-manager',manager_list,name='View-manager'),
    path('download_excel',download_excel,name='download_excel'),
    path('Error',error_page,name='Error-Page'),


    path('update-event-data/<int:event_id>/',update_event_data,name='Update_event_data'),
    path('update-manager/<uuid:manager_id>/',update_manager,name='Update_Manager'),
    path('delete-event/<int:event_id>/',delete_event,name='delete_event'),
    path('Event-Data-API',EventDataAPI.as_view(),name = 'Event_Data_API'),
    path('Handler-Delete/<uuid:handler_id>/',delete_handler,name='Handler-Delete'),


    # path('plot/',plot_chart, name='plot_view'),
    # path('pie',pie_chart,name='pie_chart'),
    path('chart',admin_chart,name='admin_chart'),



]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)