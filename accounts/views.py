from django.shortcuts import render
from django.shortcuts import render, redirect, HttpResponse
from django.conf import settings
# Create your views here.
from django.db import IntegrityError
import urllib.parse
import requests
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.contrib import messages
from instructor.models import instructorRegister, courseCreateFirstStep, landingPage, Pricing, publishCourse, Module
from learner.models import addCartModel, addWishlistedModel, purchaseCourseModel
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from category.models import Category
import json
from django.http import JsonResponse


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
 
 
def showCategoryCourse(request):
    sendData = []
    pubCourse = publishCourse.objects.all()
    if request.method == 'POST':
        try: 
            data = json.loads(request.body)
            categoryFind = Category.objects.get(category_name = data.get('category'))
            categoryCourseShow = publishCourse.objects.filter(course__category = categoryFind)
            datasend = []
            for i in categoryCourseShow:
                datasend.append({
                    'title': i.course.title,
                    "image": i.landing_page.coure_image.url,
                    "main_price":i.pricing.main_price,
                    "percent":  i.pricing.discount_percent,
                    "after_discount": i.pricing.after_discount_price,   
                    "instructor": i.course.instructor.user.first_name,
                    "uid": i.course.uid,
                })
            return JsonResponse(datasend, safe=False)

        except json.JSONDecodeError:
            return redirect('home')
            # return JsonResponse({'error': 'Invalid JSON'}, status=400)
    
    
    for i in pubCourse:
        sendData.append({
            'title': i.course.title,
            "image": i.landing_page.coure_image.url,
            "main_price":i.pricing.main_price,
            "percent":  i.pricing.discount_percent,
            "after_discount": i.pricing.after_discount_price,   
            "instructor": i.course.instructor.user.first_name,
            "uid": i.course.uid,
        })
    return JsonResponse(sendData, safe=False)


def homeView(request):
    isInstructorActive = False
    purCourse = purchaseCourseModel.objects.filter(user=request.user.id)
    pubCourse = publishCourse.objects.all()
    category = Category.objects.all()
    lst = []
    for i in purCourse:
        for j in i.course.all():
            lst.append(j.id)
    temp = []
    for i in pubCourse:
        if i.id not in lst:
            print(i.id, lst)
            temp.append(i)
  
    cartLen = 0
    if request.user:
        cartItem = addCartModel.objects.filter(user = request.user.id)
        cartLen += len(cartItem)
        try:
            instructor = instructorRegister.objects.get(user = request.user.id)
            isInstructorActive = instructor.terms_conditions
        except instructorRegister.DoesNotExist:
            isInstructorActive = False


    context ={
        'isInstructorActive': isInstructorActive,
        'cartlen': cartLen,
        'pubCourse': temp,
        'category':category,
    }
    
    return render(request, 'home.html', context)


def signUpPageView(request):
    url = (request.GET.get('next', '/'))
    if request.method == 'POST':
        name = request.POST.get('name')
        email =  request.POST.get('email')
        password =  request.POST.get('password')
        confirm_password =  request.POST.get('password2')
        if len(password) < 6 :
            messages.error(request, "you don't password less than 6")
            return redirect('signup')
        if password != confirm_password:
            messages.error(request, 'Password and confirm password do not match.')
            return redirect('signup')
        try:
            if  User.objects.get(username = email).email == email:
                messages.error(request,'Already use this email.')
                return redirect('signup')
        except User.DoesNotExist:
            user, created = User.objects.get_or_create(username = email, first_name = name, email=email)
            user.set_password(password)
            user.save()
            
        login(request, user)
        return redirect('http://127.0.0.1:8000'+url)
    return render(request, 'signup.html')

#  Login View
def loginView(request):
    url = (request.GET.get('next', '/'))
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=email)
        except User.DoesNotExist:
            user = None

        if user:
            user = authenticate(request, username=user.username, password=password)
        
        print(user)
        if user:
            login(request, user)
            return redirect('http://127.0.0.1:8000'+url)
        else:
            messages.error(request, 'Login Email or password not valid.')


    return render(request, 'login.html')

# Logout View
def logoutView(request):
    url = (request.GET.get('next', '/'))
    logout(request)
    return redirect('http://127.0.0.1:8000'+url)

# ### details course page
def detailsCoursePageView(request, uid):
    cartLen = 0
    if request.user:
        cartItem = addCartModel.objects.filter(user = request.user.id)
        cartLen += len(cartItem)
    try:
        course = publishCourse.objects.get(course__uid = uid)
    except publishCourse.DoesNotExist:
        pass
    lerner = []
    print(course)
    lerner.append(course.intended_lerner.student_learn_1)
    lerner.append(course.intended_lerner.student_learn_2)
    lerner.append(course.intended_lerner.student_learn_3)
    lerner.append(course.intended_lerner.student_learn_4)
    module = Module.objects.filter(course= course.course)

    if request.method == 'POST':
        cart = request.POST.get('add-cart')
        print(cart)
        if cart == 'cart':
            try:
                cartModel = addCartModel.objects.get( publish_course = course, user = request.user)
                messages.error(request, "Already added to cart")
                return redirect('course_details', uid)
            except addCartModel.DoesNotExist:
                addCartModel.objects.create( publish_course = course, user = request.user, quantity = 1 )
                messages.success(request, 'Successfully added to cart')
                return redirect('course_details', uid)

        else:
            try:
                wishListModel = addWishlistedModel.objects.get(publish_course = course, user = request.user)
                messages.error(request, "Already added to wishlist")
                return redirect('course_details', uid)
            except addWishlistedModel.DoesNotExist:
                addWishlistedModel.objects.create( publish_course = course, user = request.user )
                messages.success(request, 'Successfully added to wishlist')
                return redirect('course_details', uid)
        
    context = {
        'course':course,
        "lerner": lerner,
        'module': module,
        'uid': course.course.uid,
        'cartlen': cartLen,
    }
    return render(request, 'details_course_page.html', context)
