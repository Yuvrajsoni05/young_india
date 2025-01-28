import uuid

from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class LoginSide(AbstractUser):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4(),editable=False)
    login_role = models.CharField(max_length=10,choices=[('Admin','Admin'),('Manager','Manager')])
    first_name = models.CharField(max_length=200,null=True)
    last_name = models.CharField(max_length=200)
    email = models.EmailField(max_length=200)
    photo = models.ImageField(upload_to='user_photo/', null=True)
    phone_number = models.CharField(max_length=15,default='Phone Number')





