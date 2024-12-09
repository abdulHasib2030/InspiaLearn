from django.urls import path
from .views import  instructor_view, instructorRegisterView, courseCreate, descriveCourseCreateView, courseCurriculum, courseIntendedLernerView, courseLandingPageView, coursePricingView, courseMessagesView, lectureDelete, previewCourseView
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('course/', instructor_view, name='instructor'),
    path('create/', instructorRegisterView, name='instructor-create'),
    path('course/create/', courseCreate, name='course-create'),
    path('course/create/<uid>/', descriveCourseCreateView, name='descrive-course'),
    path('course/create/<uid>/curriculum/', courseCurriculum, name='curriculum'),
    path('course/create/<uid>/intended-learner/', courseIntendedLernerView, name='intended_lerner'),
    path('course/create/<uid>/<int:pk>/intended-learner-edit/', courseIntendedLernerView, name='intended_lerner_edit'),
    path('course/create/<uid>/lending-page/', courseLandingPageView, name='landing_page'),
    path('course/create/<uid>/pricing/', coursePricingView, name='pricing'),
    path('course/create/<uid>/messages/', courseMessagesView, name='messages'),
    path('preview-course/<uid>/', previewCourseView, name='preview_course'),
    path('preview-course/<uid>/<slug:slug>/', previewCourseView, name='preview_course'),

    path('lecture-delete/<uid>/<int:lectureId>/', lectureDelete, name='lecture_delete'),
]
if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)