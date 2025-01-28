from django.conf import settings
from django.urls import path
from .views import *
from django.conf.urls.static import static

urlpatterns = [
        path('manager-login',manager_login,name='manager-login'),
        path('manager-signup',manager_signup,name='manager-signup'),
        path('manager-dashboard',manager_dashboard,name='manager-dashboard'),
        path('manager-profile',manager_profile,name='manager-profile'),
        path('manager-update/<uuid:manager_id>/',manager_update,name='manager-update'),
        path('event-list',event_list,name='event-list'),
        path('event-delete/<int:events_id>/',delete_event_user,name='delete-event-user'),
        path('event_update/<int:update_id>/',update_event_data,name='update-event-data'),
        path('event_data',event_data,name='event_data'),
        path('manager-logout',manager_logout,name='manager-logout'),
        path('manager-password',manager_password,name='manager-password'),
        path('chart-dashboard',chart,name='chart-dashbaord'),
        path('pie-chart',pie_chart,name='pie-chart-data'),
        path('stackholder-chart',stackholder_chart,name='stackholder-chart'),
        path('project-verticals-chart',project_chart,name='project-vertical-chart'),
        path('about_yi',about_yi,name='about_yi'),




]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

