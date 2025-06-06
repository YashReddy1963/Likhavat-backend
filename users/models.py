from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils import timezone
from django.contrib.auth.models import User
import uuid

# Create your models here.

# User model
class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email is required")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        
        return user
    
class User(AbstractBaseUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    bio = models.TextField(blank=True, null=True)
    email = models.EmailField(unique=True)
    social_links = models.JSONField(blank=True, null=True)
    profile_image = models.ImageField(upload_to="profiles/", blank=True, null=True)
    banner_image = models.ImageField(upload_to="banners/", blank=True, null=True)
    joined_at = models.DateTimeField(default=timezone.now)
    is_verified = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return self.email
    
# OTP model
class OTP(models.Model):
    name = models.ForeignKey('User', on_delete=models.CASCADE)
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_expired(self):
            return timezone.now() > self.created_at + timezone.timedelta(minutes=10)
    
    def __str__(self):
         return f"{self.name.email} - {self.otp}"
    
# Comment model
class Comment(models.Model):
    blog = models.ForeignKey("blogs.Blogs", on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    parent = models.ForeignKey("self", null=True, blank=True, related_name="replies", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
         return f"{self.user.name} - {self.content[:30]}"
    
# Followers model
class Follow(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followers')
    followed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
         unique_together = ('follower','following')