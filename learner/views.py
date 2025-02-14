from django.shortcuts import render, redirect
from instructor.models import publishCourse, Module, Video
from learner.models import addCartModel, addWishlistedModel, purchaseCourseModel
from django.contrib.auth.models import User
# Create your views here.
from django.contrib import messages
from accounts.models import UserProfile

# def addCartView(request, id):

def cartDataView(request):
    cartLen = 0
    wishLen = 0
    if request.user:
        cartItem = addCartModel.objects.filter(user = request.user.id)
        wishListItem = addWishlistedModel.objects.filter(user = request.user.id)
        cartLen += len(cartItem)
        wishLen += len(wishListItem)
    lectureTotal = []
    total, discount, percent = 0, 0, 0
    for i in cartItem:
        total += int(i.publish_course.pricing.after_discount_price.split('.')[0])
        discount += (int(i.publish_course.pricing.main_price))
        module = Module.objects.filter(course = i.publish_course.course)
        for j in module:
            lectureTotal.append(len(j.videos.all()))
    lectureWishlist = []
    for i in wishListItem:
        module = Module.objects.filter(course = i.publish_course.course)
        for j in module:
            lectureWishlist.append(len(j.videos.all()))

  
    if total > 0 or discount > 0:
        percent += 100 -((total/ discount) * 100)


    if request.method == 'POST':
        data = request.POST.get('data', '').split()
        if data:
            if data[1] == 'wish':
                cartitem = addCartModel.objects.get(id = int(data[0]))
                try:
                    wishlist = addWishlistedModel.objects.get(publish_course = cartitem.publish_course, user = request.user)
                    messages.info(request, "Already this item added wishlist")
                    return redirect('cart')
                except addWishlistedModel.DoesNotExist:
                    addWishlistedModel.objects.create(publish_course = cartitem.publish_course, user = request.user)
                    cartitem.delete()
                    messages.success(request, "Successfully added wishlist")
                    return redirect('cart')
            else:
                wishlist = addWishlistedModel.objects.get(id = int(data[0]))
                try:
                    cartitem = addCartModel.objects.get(publish_course = wishlist.publish_course, user = request.user)
                    messages.info(request, "Already this item added cart")
                    return redirect('cart')
                except addCartModel.DoesNotExist:
                    addCartModel.objects.create(publish_course = wishlist.publish_course, user = request.user,  quantity = 1)
                    wishlist.delete()
                    messages.success(request, "Successfully added cart")
                    return redirect('cart')

        checkout = request.POST.get('checkout','') 
        if checkout:
            purchanseItem = purchaseCourseModel(user = request.user, main_price = total, discount = discount,percent = percent )
            purchanseItem.save()
            for i in cartItem:
                purchanseItem.course.add(i.publish_course) 
                i.publish_course.user = request.user
                i.publish_course.save()
            cartItem.delete()

            return redirect('learning-page')
    try:
        user_profile = UserProfile.objects.get(user = request.user.id)
    except UserProfile.DoesNotExist:
        user_profile = None
    wishListItem = zip(wishListItem, lectureWishlist)
    cartItem = zip(cartItem, lectureTotal)

   
    context = {
        'cartlen': cartLen,
        'wishlen': wishLen,
        'cartItem': cartItem,
        'total':total,
        'discount': discount,
        'percent':percent,
        'wishListItem':wishListItem,
        'user_profile':user_profile,

    }
    
    return render(request, 'cart.html', context)


def deleteCartItem(request, id):

    cartItem = addCartModel.objects.get(id = id)
    cartItem.delete()
    messages.success(request, "Successfully Deleted Cart Item")
    return redirect('cart')

def deleteWishItem(request, id):
    wishItem = addWishlistedModel.objects.get(id = id)
    next = request.GET.get('step', '/')
    if next == 'cart':
        wishItem.delete()
        messages.success(request, "Successfully Deleted Wishlist Item")
        return redirect('cart')
    else:
        wishItem.delete()
        messages.success(request, "Successfully Deleted Wishlist Item")
        return redirect('wishlist')
    

def addRemoveCartWishView(request, id):

    if request.method == 'POST':
        data = request.POST.get('data')
        print(data)
    return redirect('cart')

def learningPageView(request):
    purchaseCourse = purchaseCourseModel.objects.filter(user = request.user.id)
    cartLen = 0
 
    cartItem = addCartModel.objects.filter(user = request.user.id)
    cartLen += len(cartItem)

    wishLen = 0
    wishItem = addWishlistedModel.objects.filter(user = request.user.id)
    wishLen += len(wishItem)
    try:
        user_profile = UserProfile.objects.get(user = request.user.id)
    except UserProfile.DoesNotExist:
        user_profile = None
    context = {
        'purchaseCourse':purchaseCourse,
        'user_profile':user_profile,
         'cartlen': cartLen,
         'wishlen':wishLen,
    }
    return render(request, 'learningPage.html', context)

def courseWathingView(request, slug, slug_ = None):
    publishcourse = publishCourse.objects.get(slug = slug)
    module = Module.objects.filter(course = publishcourse.course)

    t = slug_
    title = ""
    first = False
    if t == None:
        for i in module:
            temp = (i.videos.first())
            t = temp.slug
            title += temp.title
            first = True
            break
    else:
        video = Video.objects.get(slug = slug_)
        t = video.slug    
        title += video.title
    video = Video.objects.get(slug = t)
    
    try:
        user_profile = UserProfile.objects.get(user = request.user.id)
    except UserProfile.DoesNotExist:
        user_profile = None
    cartLen = 0
 
    cartItem = addCartModel.objects.filter(user = request.user.id)
    cartLen += len(cartItem)
    wishLen = 0
    wishItem = addWishlistedModel.objects.filter(user = request.user.id)
    wishLen += len(wishItem)
    context = {
        'publishcourse': publishcourse,
        'video': video,
        'title': title,
        'module': module,
        'first':first,
        'user_profile':user_profile,
         'cartlen': cartLen,
         'wishlen': wishLen,
        
    }
    return render(request, 'watchingCourse.html', context)

def wishListView(request):
    wishlistItem = addWishlistedModel.objects.filter(user = request.user.id)
    cartLen = 0
    wishLen = 0
    wishLen+= len(wishlistItem)
    cartItem = addCartModel.objects.filter(user = request.user.id)
    cartLen += len(cartItem)
    context = {
        'wishlistItem':wishlistItem,
        'cartlen': cartLen,
        'wishlen':wishLen,
    }

    return render(request, 'learningPage.html', context)