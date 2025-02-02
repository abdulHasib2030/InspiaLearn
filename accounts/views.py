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
from instructor.models import instructorRegister, courseCreateFirstStep, landingPage, Pricing, publishCourse, Module, Video
from learner.models import addCartModel, addWishlistedModel, purchaseCourseModel, reviewCourse
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from category.models import Category
import json
from django.http import JsonResponse
import re
from accounts.models import UserProfile
from django.db.models import Avg
from django.core.mail import send_mail

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

    email = user_info['email']
    first_name = user_info['given_name']
    last_name = user_info['family_name']

    # Check if the user exists, otherwise create a new user
    try: 
        existing_usr = User.objects.get(email = email)
        login(request, existing_usr)
        return redirect('http://127.0.0.1:8000'+url)
    except User.DoesNotExist:
        user, created = User.objects.get_or_create(username=email, defaults={'first_name': first_name+' ' +last_name, 'email': email})
        UserProfile.objects.create(user=user)
        login(request, user)
    
        return redirect('http://127.0.0.1:8000'+url)
 
 
def showCategoryCourse(request):
    sendData = []
    pubCourse = publishCourse.objects.filter(admin_aprove=True)
    if request.method == 'POST':
        try: 
            data = json.loads(request.body)
            categoryFind = Category.objects.get(category_name = data.get('category'))
            categoryCourseShow = publishCourse.objects.filter(course__category = categoryFind, admin_aprove=True)
            print(len(categoryCourseShow))
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
            print(datasend)
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

    # purCourse = purchaseCourseModel.objects.filter(user=request.user.id)
    # purCourse = purchaseCourseModel.objects.all()
    pubCourse = publishCourse.objects.filter(admin_aprove=True)
    category = Category.objects.all()
    
    # lst = []
    # for i in purCourse:
    #     for j in i.course.all():
    #         lst.append(j.id)
    # temp = []
    # for i in pubCourse:
    #     if i.id not in lst:
    #         print(i.id, lst)
    #         temp.append(i)
  
    cartLen = 0
    ratingAvg = []
    temp = []
    for i in pubCourse:
        average_rating = i.reviews.aggregate(Avg('rating_star'))['rating_star__avg']
        # Handle cases where no reviews exist
        average_rating = average_rating if average_rating else 0
        ratingAvg.append(int(average_rating))
        temp.append([int(average_rating), i])
        # print(i, int(average_rating))
    
    # sorted_data = sorted(temp, key=lambda x: x[0], reverse=True)
    # print(sorted_data)
    # zipped_data = zip(temp, ratingAvg)
    sorted_data = sorted(temp, key=lambda x: x[0], reverse=True)
    query, rat =[],[]
    for i in sorted_data:
        rat.append(i[0])
        query.append(i[1])
    
    


    cartItem = addCartModel.objects.filter(user = request.user.id)
    cartLen += len(cartItem)
    wishLen = 0
    wishItem = addWishlistedModel.objects.filter(user = request.user.id)
    wishLen += len(wishItem)

    try:
        user_profile = UserProfile.objects.get(user = request.user.id)
    except UserProfile.DoesNotExist:
        user_profile = None
    reviewData = reviewCourse.objects.filter(rating_star__gte = 4 )
    zipCourseRating = zip(query, rat)
    # for i in sorted_data:
    #     for j in i:
    #         print(j)
    context ={
        'cartlen': cartLen,
        'pubCourse': pubCourse,
        'category':category,
        'user_profile':user_profile,
        'wishlen':wishLen,
        'reviewData':reviewData,
        'rating_range': range(1, 6),
        'ratingAvg':zipCourseRating,
    }
    
    return render(request, 'home.html', context)


def signUpPageView(request):
    if request.user.is_authenticated:
        return redirect('home')
    url = (request.GET.get('next', '/'))
    if request.method == 'POST':
        name = request.POST.get('name')
        email =  request.POST.get('email')
        password =  request.POST.get('password')
        confirm_password =  request.POST.get('password2')
        request.session['name'] = name
        request.session['email'] = email
        if (name == ''):
            messages.error(request, "Provide your name.")
            return redirect('signup')
        if (email == ''):
            messages.error(request, "Provide email address")
            return redirect('signup')
        pattern = r"^(?=.*[a-z])(?=.*[A-Z]).{6,}$"
        if len(password) < 6 or bool(re.match(pattern, password)) == False:
            messages.error(request, "Password must meet one Uppercase, lowercase letter and at least 6 chanacters long.")
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
            UserProfile.objects.create(user=user)

            
            login(request, user)
            return redirect(env('BASE_URL_')+url)
    name = request.session.get('name')
    email = request.session.get('email')
    context = {
       "name": name,
       "email": email
    }
    return render(request, 'signup.html', context)

#  Login View
def loginView(request):
    url = (request.GET.get('next', '/'))
    if request.user.is_authenticated:
        return redirect('home')
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
            # return redirect(env('BASE_URL_')+url)
            return redirect('/')
        else:
            messages.error(request, 'Login Email or password not valid.')


    return render(request, 'login.html')

# Logout View
def logoutView(request):
    # url = (request.GET.get('next', '/'))
    logout(request)
    # return redirect(env('BASE_URL_')+url)
    return redirect('/')

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
    # print(course)
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
    cart_disable = False
    try:
        purchase_course_usr = purchaseCourseModel.objects.get(course = course, user__user = request.user.id)
        print(purchase_course_usr)
        cart_disable = True
    except purchaseCourseModel.DoesNotExist:
        cart_disable = False
    try:
        user_profile = UserProfile.objects.get(user = request.user.id)
    except UserProfile.DoesNotExist:
        user_profile = None

    wishLen = 0
    wishItem = addWishlistedModel.objects.filter(user = request.user.id)
    wishLen += len(wishItem)
    context = {
        'course':course,
        "lerner": lerner,
        'module': module,
        'uid': course.course.uid,
        'cartlen': cartLen,
        'cart_disable':cart_disable,
        'user_profile':user_profile,
        'wishlen':wishLen,
    }
    return render(request, 'details_course_page.html', context)


def profileView(request):
    wishLen = 0
    wishItem = addWishlistedModel.objects.filter(user = request.user.id)
    wishLen += len(wishItem)
    cartLen = 0
    cartItem = addCartModel.objects.filter(user = request.user.id)
    cartLen += len(cartItem)
    if(request.user.is_authenticated):
        try:
            user_profile = UserProfile.objects.get(user = request.user)
        except UserProfile.DoesNotExist:
            user_profile = None
        return render(request, 'profile.html', {'user_profile': user_profile, 'wishlen':wishLen, 'cartlen': cartLen})
    return redirect('home')

def profileUpdate(request):
    try:
        user = User.objects.get(username = request.user.email)
        user_profile = UserProfile.objects.get(user= user)
    except UserProfile.DoesNotExist:
        user_profile = None

    if request.method == 'POST':
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        image = request.FILES.get('image', '')
        facebook = request.POST.get('facebook', '')
        linkedin = request.POST.get('linkedin', '')
        # print(facebook)
        print(image, "image for user")
        if not name:
            messages.error(request, "Can't empty name field.")
            return redirect('profile-update')
        if not email:
            messages.error(request, "Can't empty email field.")
            return redirect('profile-update')
        
        filter_user = User.objects.exclude(email = user.email )
        for i in filter_user:
            print(i.email)
            if email == i.email:
                messages.error(request, "This email already exit.")
                return redirect('profile-update')
        user.email = email
        user.username = email
        user.first_name = name
        user.save()
        if user_profile == None and image:
            UserProfile.objects.create(user = user,  profile_img = image, facebook = facebook, linkdin = linkedin)
            messages.success(request, "Updated successfully.")
            return redirect("profile")
        
        if image:
            user_profile.profile_img = image
        user_profile.facebook = facebook
        user_profile.linkdin = linkedin
        user_profile.save()
        messages.success(request, "Updated successfully.")
        return redirect("profile")
        
        
    wishLen = 0
    wishItem = addWishlistedModel.objects.filter(user = request.user.id)
    wishLen += len(wishItem)
    cartLen = 0
    cartItem = addCartModel.objects.filter(user = request.user.id)
    cartLen += len(cartItem)
        
    return render(request, 'updateProfile.html', {'user_profile': user_profile, 'wishlen': wishLen, 'cartlen': cartLen})


def adminApproveCourseView(request, uid, slug=None):
    try:
        course = publishCourse.objects.get(slug=uid)
    

        if request.method == 'POST':
            approve_level = request.POST.get('approve-level', '')
            approve_msg = request.POST.get('approve-msg', '')
            print(approve_level, approve_msg)
            if not approve_level:
                messages.error(request, "Select approve level.")
                if slug:
                    return redirect('admin-video', uid=uid, slug=slug)
                return redirect('admin', uid=uid)
            
            if approve_level == 'approve':
                approve_msg = approve_msg if approve_msg else "Successfully approved your course"
              
                course.course.publish_true=True
                course.admin_aprove = True
                course.admin_text = approve_msg
                course.save_base()
                course.course.save()
                # course.asave()
                print(course.course.publish_true)
            
                send_mail(f'Admin approval for {course.landing_page.title}', approve_msg, 'abdulhasib2030@gmail.com', [course.course.instructor.user.email,])
                messages.success(request, "Successfully appoved course. Sending user mail.")
                if slug:
                    return redirect('admin-video', uid=uid, slug=slug)
                return redirect('admin-page', uid=uid)
            else:
                approve_msg = approve_msg if approve_msg else "Admin declined your course"
                course.course.publish_true=False
                course.admin_aprove =False
                course.admin_text = approve_msg
                course.save_base()
                course.course.save()
                send_mail(f'Admin approval for {course.landing_page.title}', approve_msg, 'abdulhasib2030@gmail.com', [course.course.instructor.user.email,])
                messages.success(request, "Successfully declined course sending user mail")
                if slug:
                    return redirect('admin-video', uid=uid, slug=slug)
                return redirect('admin-page', uid=uid)

        lerner = []

        lerner.append(course.intended_lerner.student_learn_1)
        lerner.append(course.intended_lerner.student_learn_2)
        lerner.append(course.intended_lerner.student_learn_3)
        lerner.append(course.intended_lerner.student_learn_4)
        module = Module.objects.filter(course= course.course)
    
    
        if slug:
            video = Video.objects.get(slug = slug)
            video = video.video_file
        else:
            video = course.landing_page.promotional_video
    except publishCourse.DoesNotExist:
        course = None
        lerner=None
        module=None
        course.course.uid=None
        video=None
    context = {
        'course':course,
        "lerner": lerner,
        'module': module,
        'uid': course.course.uid,
        'video': video
    }
    return render(request, 'admin_approve.html', context)
