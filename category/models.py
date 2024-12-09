from django.db import models
from django.utils.text import slugify
from django.urls import reverse

# Create your models here.
class Category(models.Model):
    category_name = models.CharField(max_length=200)
    category_image = models.FileField(upload_to='category')
    slug = models.SlugField(max_length=300)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.category_name)
        super(Category, self).save(*args, **kwargs)
    def get_url(self):
        return reverse('category_url', args=[self.slug])

