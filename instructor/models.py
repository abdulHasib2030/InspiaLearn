from django.db import models
from django.contrib.auth.models import User
from category.models import Category
# from moviepy.editor import VideoFileClip
from moviepy import VideoFileClip
import os
from django.utils.text import slugify

# Create your models here.
EXPERIENCE = (('beginner', 'beginner'),
              ('intermediate', 'intermediate'),
              ('expert', 'expert'))
class instructorRegister(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    teaching_before = models.CharField(max_length=200, null=True)
    experience = models.CharField(max_length= 100, choices=EXPERIENCE, null=True)
    terms_conditions = models.BooleanField(default=False, null=True)
    
class courseCreateFirstStep(models.Model):
    instructor = models.ForeignKey(instructorRegister, on_delete= models.CASCADE)
    title = models.CharField(max_length=70)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    time = models.CharField(max_length=100)
    dateTime = models.DateTimeField(auto_now_add=True)
    uid = models.CharField(max_length= 50, null= True)
    publish_true = models.BooleanField(default= False, null= True)

class intendedLearner(models.Model):
    course = models.OneToOneField(courseCreateFirstStep, on_delete= models.CASCADE)
    course_requirement = models.CharField(max_length=1000, null= True)
    student_learn_1 = models.CharField(max_length= 200, null=True )
    student_learn_2 = models.CharField(max_length= 200, null=True)
    student_learn_3 = models.CharField(max_length= 200, null=True)
    student_learn_4 = models.CharField(max_length= 200, null=True)
    who_this_course = models.CharField(max_length= 1000, null=True)

class Module(models.Model):
    course = models.ForeignKey(courseCreateFirstStep, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    position = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['position']

    def __str__(self):
        return self.title

class Video(models.Model):
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name='videos')
    title = models.CharField(max_length=255)
    video_file = models.FileField(upload_to='videos/', blank=True, null=True) 
    duration = models.CharField(max_length=100, blank=True, null=True)
    position = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    slug = models.SlugField(blank=True, null=True)

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
         # Save the file first
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            count = 1
            while Video.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{count}"
                count += 1
            self.slug = slug
            super(Video, self).save(*args, **kwargs) 


        # Get the full path of the uploaded file
        video_path = self.video_file.path
        try:
            # Extract video duration using moviepy
            clip = VideoFileClip(video_path)
            dur = clip.duration  # Duration in seconds
            minutes, seconds = divmod(dur, 60)
            self.duration = f"{int(minutes):02d}:{int(seconds):02d}"
            clip.close()
        except Exception as e:
            print(f"Error calculating duration: {e}")
            self.duration = None

        super().save(*args, **kwargs)  # Save again with duration

LEVEL =(('beginner', 'beginner'),
        ('intermediate', 'intermediate'),
        ('expert', 'expert'),
        ('all', 'all'))
class landingPage(models.Model):
    course = models.OneToOneField(courseCreateFirstStep, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    course_subtitle = models.CharField(max_length=150, null=True)
    course_description = models.TextField()
    level = models.CharField(max_length= 50, choices=LEVEL)
    # category = models.ForeignKey(Category, on_delete=models.CASCADE)
    coure_image = models.FileField(upload_to='course_image/')
    promotional_video = models.FileField(upload_to='promotional_video/')
    
class Pricing(models.Model):
    course = models.OneToOneField(courseCreateFirstStep, on_delete= models.CASCADE)
    main_price = models.CharField(max_length=200)
    discount_percent = models.CharField(max_length=200)
    after_discount_price = models.CharField(max_length=200)

class welcomeCongratMessages(models.Model):
    course = models.OneToOneField(courseCreateFirstStep, on_delete= models.CASCADE)
    welcomeMsg = models.CharField(max_length=1000)
    congratMsg = models.CharField(max_length=1000)

class publishCourse(models.Model):
    course = models.OneToOneField(courseCreateFirstStep, on_delete=models.CASCADE)
    intended_lerner = models.OneToOneField(intendedLearner, on_delete=models.CASCADE)
    landing_page = models.OneToOneField(landingPage, on_delete=models.CASCADE)
    pricing = models.OneToOneField(Pricing, on_delete=models.CASCADE)
    msg = models.OneToOneField(welcomeCongratMessages, on_delete=models.CASCADE)
    video_length = models.CharField(max_length= 200, null=True, blank=True)
    # purchanse_course = models.BooleanField(default=False, null= True)
    slug = models.SlugField(blank=True, null=True)
    totalLecture = models.CharField(max_length=200, null= True)
    admin_aprove = models.BooleanField(default=False, null=True,)
    admin_text = models.TextField(max_length=500, null=True)

    def save(self, *args, **kwargs):
         # Save the file first
        if not self.slug:
            base_slug = slugify(self.course.title)
            slug = base_slug
            count = 1
            while courseCreateFirstStep.objects.filter(title=slug).exists():
                slug = f"{base_slug}-{count}"
                count += 1
            self.slug = slug
            super(publishCourse, self).save(*args, **kwargs) 
