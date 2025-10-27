from django.db import models
from django.contrib.auth.models import AbstractUser,UserManager




class CustomUserManager(UserManager):
    
    def _create_user(self, email, password, **extra_fields):
        """
        Create and save a user with the given email and password.
        """
        
        
        if not email:
            raise ValueError('The Email field must be set')
        
        email = self.normalize_email(email)
        
        if 'username' not in extra_fields:
            extra_fields['username'] = email.split('@')[0]
        
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        
        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    username = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField(unique=True)

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = [] 
    
    objects = CustomUserManager()

    def __str__(self):
        return self.email
    
    @property
    def is_general_user(self):
        return self.is_staff and self.is_superuser