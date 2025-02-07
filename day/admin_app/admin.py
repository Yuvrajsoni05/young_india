from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(LoginSide)
admin.site.register(Login_Role)

admin.site.site_title = "YI Dashboard"
admin.site.site_header = "Young India"
admin.site.index_title = "Models "