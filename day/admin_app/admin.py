from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(Login_Role)

admin.site.site_title = "YI Dashboard"
admin.site.site_header = "Young India"
admin.site.index_title = "Models "



class LoginSideAdmin(admin.ModelAdmin):
    list_display = ("first_name" , "last_name", "username" , "email","get_login_role","phone_number",)



    def get_login_role(self, obj):
        
        return ", ".join([i.name for i in obj.login_role.all()
                            
                          
                          ])
    
    get_login_role.short_description = 'login_Role'

admin.site.register(LoginSide,LoginSideAdmin)