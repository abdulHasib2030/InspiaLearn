from django.contrib import admin
from learner.models import addCartModel,addWishlistedModel, purchaseCourseModel, reviewCourse
# Register your models here.

admin.site.register(addCartModel)
admin.site.register(addWishlistedModel)
admin.site.register(purchaseCourseModel)
admin.site.register(reviewCourse)
