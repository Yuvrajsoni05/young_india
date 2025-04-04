from tkinter.font import names

from django.conf import settings
from django.urls import path
from .views import *
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from .views import EventDataAPI

urlpatterns = [
    path("", index, name="index"),
    # path('Admin-Login',Admin_Login,name='Admin_Login'),
    path("New-EC-Member", Admin_Signup, name="Admin_Signup"),
    path("Admin-Dashboard", Admin_Dashboard, name="Admin_Dashboard"),
    path("Admin-Profile", Admin_Profile, name="Admin_Profile"),
    path("Admin-Update/<uuid:admin_id>/", Admin_update, name="Admin_Update"),
    path("Admin-Password", admin_password, name="Admin_Password"),
    path("Admin-Logout", admin_logout, name="Admin_Logout"),
    # path('Event-List',Event_list,name='Event_List'),
    path("EC-Member-List", manager_list, name="View-manager"),
    # path('Ec-member',Ec_Member,name=Ec),
    path("download_excel", download_excel, name="download_excel"),
    path("Error", error_page, name="Error-Page"),
    path("admin-event-data", admin_event_data, name="admin_event_data"),
    # path('header',header,name='header')
    # path('role_list',Role_List, name="Role_List"),
    path(
        "update-event-image/<int:image_id>/", event_image_delete, name="event_image_id"
    ),
    path(
        "update-event-data/<int:event_id>/", update_event_data, name="Update_event_data"
    ),
    path("update-manager/<uuid:manager_id>/", update_memeber, name="Update_Manager"),
    path("delete-event/<int:event_id>/", delete_event, name="delete_event"),
    path("Event-Data-API", EventDataAPI.as_view(), name="Event_Data_API"),
    path("Member-Delete/<uuid:member_id>/", delete_member, name="Member-Delete"),
    # path('plot/',plot_chart, name='plot_view'),
    # path('getuser',getuser,name='getuser'),
    path("chart", admin_chart, name="admin_chart"),
    path("password_reset/", CustomPasswordResetView.as_view(), name="password_reset"),
    path(
        "password_reset_done/",
        CustomPasswordResetDoneView.as_view(),
        name="password_reset_done",
    ),
    path(
        "reset/<uidb64>/<token>/",
        CustomPasswordResetConfirm.as_view(),
        name="password_reset_confirm",
    ),
    path("reset_done/", password_update_done, name="password_reset_complete"),
    path("member_diary",members_diary,name="member_diary"),
    # path('api/get-user-details/', get_logged_in_user_details, name='get-user-details'),
    # path('get-username/',get_username, name='get_username'),
    # path('delete_events/',delete_multiple_events, name='delete_multiple_events'),
    # path('vertical_base', vertical_base,name='vertical_base')
]
[]
