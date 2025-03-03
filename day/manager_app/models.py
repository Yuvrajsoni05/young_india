import uuid

from django.db import models
from admin_app.models import LoginSide
# Create your models here.





class Event_Data(models.Model):
    # id  =  models.UUIDField(primary_key=True,default=uuid.UUID,editable=True)
    user = models.ForeignKey(LoginSide, on_delete=models.SET_NULL, null=True,db_index=True)
    your_name = models.CharField(max_length=50)
    event_name = models.CharField(max_length=200,blank=True)
    event_venue = models.CharField(max_length=200,blank=True)
    event_expense = models.BigIntegerField(blank=True,default=0)
    date = models.DateField()
    role_yi = models.CharField(max_length=200)
    project_vertical = models.CharField(max_length=200)
    project_stakeholder = models.CharField(max_length=200)
    yi_pillar = models.CharField(max_length=200)
    social_link = models.URLField(max_length=300)
    which_SIG = models.CharField(max_length=200,blank=True,null=True)
    event_handle = models.CharField(max_length=200,blank=True,null=True)
    total_impact = models.BigIntegerField(blank=True,default=1)
    # event_photo = models.ImageField(upload_to='event_photo/',null=True)
    # place_name = models.CharField(max_length=200,blank=True)
    school = models.CharField(max_length=200,blank=True,null=True)
    collage = models.CharField(max_length=200,blank=True,null=True)
    associate_partner = models.CharField(max_length=200,null=True,blank=True)


class Event_Image(models.Model):
    event = models.ForeignKey(Event_Data,related_name='event_photo',on_delete=models.CASCADE)
    event_photo = models.ImageField(upload_to='event_photo/',null=True,blank=True)







