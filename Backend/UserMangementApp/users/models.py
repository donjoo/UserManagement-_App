import profile
from django.db import models
from django.contrib.auth.models import AbstractBaseUser , BaseUserManager
from django.utils import timezone
# Create your models here.


class MyAccountManager(BaseUserManager):
    def create_user(self, first_name , last_name, username ,email , phone_number , password = None):
        if not email:
            raise ValueError('User must have an email address ')
        if not username:
            raise ValueError('User must have an username')

        user = self.model(
            email = self.normalize_email(email),
            username = username,
            first_name = first_name,
            last_name= last_name,
            phone_number = phone_number,
        )
        user.set_password(password)
        user.save(using=self.db)
        return user
    
    def create_superuser(self, first_name, last_name, email, username, password):
        user = self.create_user(
            email = self.normalize_email(email),
            username= username,
            password= password,
            first_name= first_name,
            last_name= last_name,
        )

        user.is_admin = True
        user.is_acive = True
        user.is_staff = True
        user.is_superadmin = True
        user.save(using=self.db)
        return user
    


class CustomUser(AbstractBaseUser):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    username = models.CharField(max_length=50,unique=True)
    email = models.EmailField(max_length=100, unique=True)
    phone_number = models.CharField(max_length=50,blank=True)

    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now_add=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superadmin = models.BooleanField(default=False)


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    objects = MyAccountManager()

    def __str__(self):
        return self.email
    
    def has_prem(self,prem, obj=None):
        return self.is_admin
    
    def has_module_perms(self, app_label):
        return True
    

class UserProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='iuser/profile_pic/', null=True,blank=True)


    def __str__(self):
        return str(self.user.first_name)