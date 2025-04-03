import uuid

from django.db import models
from admin_app.models import LoginSide
# Create your models here.





class Event_Data(models.Model):
    # id  =  models.UUIDField(primary_key=True,default=uuid.UUID,editable=True)
    user = models.ForeignKey(LoginSide, on_delete=models.SET_NULL, null=True,db_index=True)
    your_name = models.CharField(max_length=50)
    event_name = models.CharField(max_length=200,blank=True)
    event_venue = models.TextField(blank=True)
    event_expense = models.BigIntegerField(blank=True,null=True,default=0)
    date = models.CharField(max_length=200)
    role_yi = models.CharField(max_length=200)
    project_vertical = models.CharField(max_length=200)
    project_stakeholder = models.CharField(max_length=200)
    yi_pillar = models.CharField(max_length=200)
    social_link = models.URLField(max_length=300)
    which_SIG = models.CharField(max_length=200,blank=True,null=True)
    event_member = models.CharField(max_length=1000,blank=True,null=True)
    total_impact = models.BigIntegerField(blank=True,default=1)
    select_ec_member = models.CharField(max_length=50,blank=True,null=True)
    # event_photo = models.ImageField(upload_to='event_photo/',null=True)
    # place_name = models.CharField(max_length=200,blank=True)
    school = models.CharField(max_length=200,blank=True,null=True)
    collage = models.CharField(max_length=200,blank=True,null=True)
    associate_partner = models.CharField(max_length=200,null=True,blank=True)
    event_description =  models.TextField(max_length=700,null=True,blank=True)
    

class Event_Image(models.Model):
    event = models.ForeignKey(Event_Data,related_name='event_photo',on_delete=models.CASCADE)
    event_photo = models.ImageField(upload_to='event_photo/',null=True,blank=True)



# receiver_email = "saium@abcinc.com"
# template_name = "email/template/path/in/template/folder/filename.html"
# convert_to_html_content =  render_to_string(
#   template_name=template_name,
#   context=context
# )
# plain_message = strip_tags(convert_to_html_content)

# yo_send_it = send_mail(
#   subject="Receiver information from a form",
#   message=plain_message,
#   from_email=settings.EMAIL_HOST_USER,
#   recipient_list=[receiver_email,]   # recipient_list is self explainatory
#   html_message=convert_to_html_content
#   fail_silently=True    # Optional
# )



