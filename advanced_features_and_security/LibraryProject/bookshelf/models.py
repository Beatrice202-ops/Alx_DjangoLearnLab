from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

# Create your models here.
class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    publication_year = models.IntegerField()

    def __str__(self):
        return self.title
    
class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('the Email must be set')
        email = self.normalize_email(email)
        user = self.models(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user
    

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get ('is_staff') is not True:
            raise ValueError("superuser must have is_staff=True")
        if extra_fields.get ('is_superuser') is not True:
            raise ValueError("superuser must have is_superuser=True")
        return self.create_user(email=email, password=password, **extra_fields)
    
           
                         
class CustomUser(AbstractUser):
    username = None
    date_of_birth = models.DateField(null=True, blank=True)
    profile_photo = models.ImageField(upload_to='', null=True, blank=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
