from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_img = models.FileField(upload_to='porfile/')
    facebook = models.CharField(max_length= 200, null=True)
    linkdin = models.CharField(max_length= 200, null=True)


