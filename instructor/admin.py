from django.contrib import admin

# Register your models here.
from instructor.models import instructorRegister, courseCreateFirstStep, intendedLearner, Module, Video, landingPage, Pricing, welcomeCongratMessages, publishCourse

admin.site.register(instructorRegister)
admin.site.register(courseCreateFirstStep)
admin.site.register(intendedLearner)
admin.site.register(Module)
admin.site.register(Video)
admin.site.register(landingPage)
admin.site.register(Pricing)
admin.site.register(welcomeCongratMessages)
admin.site.register(publishCourse)
