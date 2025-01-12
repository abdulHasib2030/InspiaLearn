from django.db import models
from instructor.models import publishCourse
from django.contrib.auth.models import User
from accounts.models import UserProfile
# Create your models here.
class addCartModel(models.Model):
    publish_course = models.ForeignKey(publishCourse, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete= models.CASCADE)
    quantity = models.IntegerField()
    active = models.BooleanField(default=False)
    
class addWishlistedModel(models.Model):
    publish_course = models.ForeignKey(publishCourse, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete= models.CASCADE)
    active = models.BooleanField(default=False)

class purchaseCourseModel(models.Model):
    course = models.ManyToManyField(publishCourse)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, null=True)
    dateTime = models.DateTimeField(auto_now_add= True)
    main_price = models.CharField(max_length=200)
    discount = models.CharField(max_length=200)
    percent = models.CharField(max_length=200)
    date = models.DateField(auto_now_add=True, null=True)

class reviewCourse(models.Model):
    user = models.ForeignKey(UserProfile, on_delete= models.CASCADE)
    publish_course = models.ForeignKey(publishCourse, on_delete=models.CASCADE, related_name='reviews')
    rating_star = models.IntegerField()
    rating_text = models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)



