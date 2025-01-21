from django.db import models
from admin_app.models import LoginSide
# Create your models here.
class Event_Data(models.Model):
    user = models.ForeignKey(LoginSide, on_delete=models.SET_NULL, null=True, default='1')

    your_name = models.CharField(max_length=200)
    date = models.DateField()
    role_yi = models.CharField(max_length=200,default='role_yi')
    project_vertical = models.CharField(max_length=200)
    project_stakeholder = models.CharField(max_length=200)
    yi_pillar = models.CharField(max_length=200)
    social_link = models.URLField(max_length=300)
    which_SIG = models.CharField(max_length=200,default='SIG')
    event_handle = models.CharField(max_length=200,)
    total_impact = models.IntegerField(blank=False)


