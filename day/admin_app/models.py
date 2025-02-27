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




# user = User.objects.get(username="your_username")
# print(user)
#  print(user.username, user.email, user.id)
# users = LoginSide.objects.filter(username='meet')

# # This will iterate over all users (in case there are multiple 'meet' users)
# for user in users:
#     print(user.username, user.email, user.id)  # Print any other fields you need
# login_data = LoginSide.objects.get(username="meet").login_role.all().values_list("name",flat=True)



# from yourapp.models import LoginSide

# # Fetch a particular user, e.g., by their email (you can adjust the condition to suit your needs)
# user = LoginSide.objects.get(email='user_email@example.com')

# # Access the related `login_role` field (ManyToMany relationship) and print the list of roles
# print(user.login_role.all())
# SessionInterrupted at /EC-Member-List
# The request's session was deleted before the request completed. The user may have logged out in a concurrent request, for example.