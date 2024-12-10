from django.urls import path
from accounts.views import google_login, oauth2callback,signUpPageView,showCategoryCourse, loginView, logoutView, detailsCoursePageView, profileView,profileUpdate
# from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('login/', loginView, name="login"),
    path('signup/', signUpPageView, name='signup'),
    path('logout/', logoutView, name='logout'),
        # path('logout/', LogoutView.as_view(next_page='/'), name='logout'),

    path('course/<uid>/', detailsCoursePageView, name='course_details'),
    path('home/catgory/', showCategoryCourse),
    path('profile/', profileView, name='profile'),
    path('profile/update', profileUpdate, name='profile-update'),

]
