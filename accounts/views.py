from django.shortcuts import render, redirect
from django.conf import settings
import urllib.parse
import requests
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
# Create your views here.


def google_login(request):
    
    base_url = 'https://accounts.google.com/o/oauth2/v2/auth'
    params = {
        'client_id': settings.GOOGLE_CLIENT_ID,
        'redirect_uri': settings.GOOGLE_REDIRECT_URI,
        'response_type': 'code',
        'scope': 'openid email profile',
        'access_type': 'offline',
        'prompt': 'consent',
    }
    url = f'{base_url}?{urllib.parse.urlencode(params)}'
    print(url)
    return redirect(url)


def oauth2callback(request):
    url = (request.GET.get('next', '/'))
    print(url)
    code = request.GET.get('code')
    if not code:
        return redirect('http://127.0.0.1:8000'+url)
    token_url = 'https://oauth2.googleapis.com/token'
    token_data = {
        'code': code,
        'client_id': settings.GOOGLE_CLIENT_ID,
        'client_secret': settings.GOOGLE_CLIENT_SECRET,
        'redirect_uri': settings.GOOGLE_REDIRECT_URI,
        'grant_type': 'authorization_code',
    }
    
    token_response = requests.post(token_url, data=token_data)
    token_json = token_response.json()
    access_token = token_json.get('access_token')
    if not access_token:
        return redirect('http://127.0.0.1:8000'+url)
    user_info_url = 'https://www.googleapis.com/oauth2/v3/userinfo'
    user_info_params = {'access_token': token_json['access_token']}
    user_info_response = requests.get(user_info_url, params=user_info_params)
    user_info = user_info_response.json()

    # You can now use the `user_info` to authenticate the user in your Django app.
    email = user_info['email']
    first_name = user_info['given_name']
    last_name = user_info['family_name']
    # print(user_info)
    # Check if the user exists, otherwise create a new user
    try: 
        existing_usr = User.objects.get(email = email)
        login(request, existing_usr)
        return redirect('http://127.0.0.1:8000'+url)
    except User.DoesNotExist:
        user, created = User.objects.get_or_create(username=email, defaults={'first_name': first_name, 'last_name': last_name, 'email': email})

    # Log the user in
        login(request, user)
    
        return redirect('http://127.0.0.1:8000'+url)
 
 

def homeView(request):
    # isInstructorActive = False
    # purCourse = purchaseCourseModel.objects.filter(user=request.user.id)
    # pubCourse = publishCourse.objects.all()
    # category = Category.objects.all()
    # lst = []
    # for i in purCourse:
    #     for j in i.course.all():
    #         lst.append(j.id)
    # temp = []
    # for i in pubCourse:
    #     if i.id not in lst:
    #         print(i.id, lst)
    #         temp.append(i)
  
    # cartLen = 0
    # if request.user:
    #     cartItem = addCartModel.objects.filter(user = request.user.id)
    #     cartLen += len(cartItem)
    #     try:
    #         instructor = instructorRegister.objects.get(user = request.user.id)
    #         isInstructorActive = instructor.terms_conditions
    #     except instructorRegister.DoesNotExist:
    #         isInstructorActive = False


    context ={
        # 'isInstructorActive': isInstructorActive,
        # 'cartlen': cartLen,
        # 'pubCourse': temp,
        # 'category':category,
    }
    
    return render(request, 'home.html', context)

