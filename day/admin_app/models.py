from urllib import request
import uuid

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.forms import ValidationError
from django.core.validators import validate_email
from django.core.validators import RegexValidator
from django.core.validators import FileExtensionValidator, ValidationError

ROLE_CHOICES = [
    ("Admin", "Admin"),
    ("Manager", "Manager"),
    ("Masoom", "Masoom"),
    ("Road Safety", "Road Safety"),
    ("Yi Health", "Yi Health"),
    ("Sports", "Sports"),
    ("Accessibility", "Accessibility"),
    ("Learning(YI Talks)", "Learning(YI Talks)"),
    ("Membership" ,"Membership"),
    ("Climate Change", "climate Change"),
    ("Innovation", "Innovation"),
    ("Entrepreneurship", "Entrepreneurship"),
    ("Branding & PR", "Branding & PR"),
    ("Women Engagement (YIWE)", "Women Engagement (YIWE)"),
    ("Culture Connect", "Culture Connect"),
    ("Yi Angel", "Yi Angel"),
    ("Thalir" , "Thalir"),
    ("Yuva" , "Yuva"),
    ("Rural Initiatives","Rural Initiatives"),
    ("General Public","General Public"),
    ("Special Interest Group (S.I.G)", "Special Interest Group (S.I.G)"),
    ("Chapter","Chapter")

]


class Login_Role(models.Model):
    name = models.CharField(max_length=200, primary_key=True, choices=ROLE_CHOICES)
    image = models.ImageField(upload_to="role_images", null=True, blank=True)

    def __str__(self):
        return f"{self.name} {self.image}"


# Create your models here.
class LoginSide(AbstractUser):

    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, db_index=True
    )
    login_role = models.ManyToManyField(Login_Role, verbose_name="LoginRole")
    first_name = models.CharField(max_length=200, null=True, verbose_name="FirstName")
    last_name = models.CharField(max_length=200)
    email = models.EmailField(max_length=200, unique=True, validators=[validate_email])
    photo = models.ImageField(upload_to="user_photo/", null=True, blank=True, validators = [FileExtensionValidator(allowed_extensions=["jpeg", "jpg", "png"])])
    yi_role = models.CharField(max_length=200, null=True)

    phone_number = models.CharField(
        max_length=10,  # This will accommodate international numbers
        default="0",
        validators=[
            RegexValidator(
                regex=r"^(\+91[\-\s]?)?[0]?(91)?[789]\d{9}$",  # This is the regex for validating the phone number
                message="Enter a valid phone number.",
                code="invalid phone",
            ),
        ],
    )

    # @property
    # def full_name(self):
    #     return f"{self.first_name} {self.last_name}"
    
    @property
    def designation(self):
        
        roles = ', '.join((role.name) for role in self.login_role.all())
        return f"{roles} {self.yi_role}"
        
    
    
    @property
    def full_name(self):
        demo = ()
        return f"{self.first_name} {self.last_name} {self.designation} "
    

    def __str__(self):
        return f"{self.first_name} | {self.last_name} | {self.login_role}"

    def delete(self, *args, **kwargs):
        self.photo.delete()
        super().delete(*args, **kwargs)
        
        
        
class Member_details(models.Model):
    First_Name = models.CharField(max_length=200 ,null=True, blank=True)
    Last_Name = models.CharField(max_length=200 ,null=True, blank=True)
    
    Email_Address = models.CharField(max_length=200 ,null=True, blank=True)
    Phone_No = models.CharField(max_length=200 ,null=True, blank=True)
    Company_Name= models.CharField(max_length=200 ,null=True, blank=True)
    Company_Designation = models.CharField(max_length=200 ,null=True, blank=True)
    Address = models.CharField(max_length=200 ,null=True, blank=True)
    EC_Member = models.CharField( max_length=200,null=True, blank=True)
    EC_Designation = models.CharField(max_length=200 ,null=True, blank=True)
    Profile_Photo = models.URLField(max_length=200 ,null=True, blank=True)
    Vertical = models.CharField(max_length=200 ,null=True, blank=True)
    DOB = models.CharField(max_length=200 ,null=True, blank=True)
    Membership_Type = models.CharField(max_length=200 ,null=True, blank=True)

    


   

#   vertical_roles = [v.strip() for v in i.Vertical.split(',')] #splits the string and removes extra spaces
    
#             roles = Login_Role.objects.filter(name__in=vertical_roles) # Corrected variable name to roles
            
#             Admin_user.login_role.set(roles)
#             Admin_user.save()

# import string

# length = 8
# random_string = ''.join(random.choices(string.ascii_letters + string.digits, k=length))
# print(random_string)

    
    
    

    # def full_name(self):
    #     return (
    #         f"{self.first_name} {self.last_name}" if self.first_name else self.last_name
    #     )


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


# Show Login Role

# user = LoginSide.objects.get(id='some-uuid')  # Replace 'some-uuid' with the actual UUID
# print(user.login_role.all())
# for role in user.login_role.all():
#     print(role.name)
# print(str(user.login_role.all()))


# python3.13.exe -m venv venv
# $ source venv/Scripts/activate
# $ pip install -r requirement.txt
