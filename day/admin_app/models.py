import uuid

from django.db import models
from django.contrib.auth.models import AbstractUser



ROLE_CHOICES = [
    ('Admin','Admin'),('Manager','Manager'),
    ('Masoom','Masoom'),('Road Safety','Road Safety'),
    ('Health','Health'),('Sports','Sports'),
    ('Accessibility','Accessibility'),('Learning(YI Talks)','Learning(YI Talks)'),
    ('Climate action','Climate action'),('Climate action','Climate action'),
    ('Innovation','Innovation'),('Entrepreneurship','Entrepreneurship'),('Branding & PR','Branding & PR'),('Women Engagement (YIWE)','Women Engagement (YIWE)'),
    ('Culture Connect','Culture Connect'),('Yi Angel','Yi Angel'),('Special Interest Group (S.I.G)','Special Interest Group (S.I.G)')

]
class Login_Role(models.Model):
    name = models.CharField(max_length=200,primary_key=True,choices=ROLE_CHOICES)

# Create your models here.
class LoginSide(AbstractUser):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    login_role = models.ManyToManyField(Login_Role,)
    first_name = models.CharField(max_length=200,null=True)
    last_name = models.CharField(max_length=200)
    email = models.EmailField(max_length=200,unique=True,)
    photo = models.ImageField(upload_to='user_photo/', null=True,)
    phone_number = models.CharField(max_length=15,default='Phone Number')





