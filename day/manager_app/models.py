from django.db import models
from admin_app.models import LoginSide
# Create your models here.





class Event_Data(models.Model):
    user = models.ForeignKey(LoginSide, on_delete=models.SET_NULL, null=True)
    your_name = models.CharField(max_length=50)
    event_name = models.CharField(max_length=200,blank=True)
    event_venue = models.CharField(max_length=200,blank=True)
    event_expense = models.IntegerField(blank=True,default=1)
    date = models.CharField(max_length=200)
    role_yi = models.CharField(max_length=200)
    project_vertical = models.CharField(max_length=200)
    project_stakeholder = models.CharField(max_length=200)
    yi_pillar = models.CharField(max_length=200)
    social_link = models.URLField(max_length=300)
    which_SIG = models.CharField(max_length=200,null=True,blank=True)
    event_handle = models.CharField(max_length=200,)
    total_impact = models.IntegerField(blank=True,default=1)
    event_photo = models.ImageField(upload_to='event_photo/',null=True)
    place_name = models.CharField(max_length=200,blank=True)
    associate_partner = models.CharField(max_length=200,null=True)





