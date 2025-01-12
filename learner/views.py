from django.shortcuts import render, redirect, get_object_or_404
from instructor.models import publishCourse, Module, Video
from learner.models import addCartModel, addWishlistedModel, purchaseCourseModel, reviewCourse
from django.contrib.auth.models import User
# Create your views here.
from django.contrib import messages
from accounts.models import UserProfile
from django.db.models import Q, Count

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
            user_p  = UserProfile.objects.get(user = request.user)
            purchanseItem = purchaseCourseModel(user = user_p, main_price = total, discount = discount,percent = percent )
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
    purchaseCourse = purchaseCourseModel.objects.filter(user__user = request.user.id)
    cartLen = 0
    print(purchaseCourse)
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

def courseWathingView(request, slug, slug_ = None, ):
    if request.user.is_authenticated:    
        publishcourse = publishCourse.objects.get(slug = slug, )
        try: 
            purchaseCourse = purchaseCourseModel.objects.filter(user__user = request.user.id)
            flg = True
            # user validate buy this course
            for j in purchaseCourse:
                for i in j.course.all():
                    if publishcourse == i:
                        
                        flg = False
                        break
                if flg == False:
                    break
            if flg:
                return redirect('/')
            
          
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

            current_video = get_object_or_404(Video, slug=t, module__course= publishcourse.course)
            course_videos = Video.objects.filter(module__course=publishcourse.course).order_by('id')
            video_list = list(course_videos)
            current_index = video_list.index(current_video)

            # Determine Next and Previous videos
            next_video = video_list[current_index + 1].slug if current_index + 1 < len(video_list) else None
            previous_video = video_list[current_index - 1].slug if current_index - 1 >= 0 else None

            try:
                user_profile = UserProfile.objects.get(user = request.user)
            except UserProfile.DoesNotExist:
                user_profile = UserProfile.objects.create(user = request.user)

            cartLen = 0
        
            cartItem = addCartModel.objects.filter(user = request.user.id)
            cartLen += len(cartItem)
            wishLen = 0
            wishItem = addWishlistedModel.objects.filter(user = request.user.id)
            wishLen += len(wishItem)

            if request.method == 'POST':
                reviewText = request.POST.get('review-text', '')
                rating = request.POST.get('rating', '')
                if not reviewText:
                    messages.error(request, "Review text data not empty.")
                    return redirect('watching_page_video', slug, current_video.slug )
                if not rating:
                    messages.error(request, "Rating can't empty.")
                    return redirect('watching_page_video', slug, current_video.slug )
                try:
                    reviewUpdate = reviewCourse.objects.get(user = user_profile,  publish_course=publishcourse)
                    reviewUpdate.rating_text = reviewText
                    reviewUpdate.rating_star = rating
                    reviewUpdate.save()
                    messages.success(request, "Updated your review.")
                    return redirect('watching_page_video', slug, current_video.slug )
                except reviewCourse.DoesNotExist:
                    review = reviewCourse.objects.create(user= user_profile, publish_course=publishcourse,  rating_star = int(rating), rating_text = reviewText)
                    review.save()
                    messages.success(request, "We accepted your review.")
                    return redirect('watching_page_video', slug, current_video.slug )
                
            try: 
                reviewData = reviewCourse.objects.get(user = user_profile, publish_course=publishcourse)
            except reviewCourse.DoesNotExist:
                reviewData = None

            context = {
                'publishcourse': publishcourse,
                'video': current_video,
                'title': title,
                'module': module,
                'first':first,
                'user_profile':user_profile,
                'cartlen': cartLen,
                'wishlen': wishLen,
                "next_lesson": next_video,
                "previous_lesson": previous_video,
                "reviewData": reviewData,
                'rating_range': range(1,6),
                
            }
            return render(request, 'watchingCourse.html', context)
        except purchaseCourseModel.DoesNotExist:
            return redirect('/')
    else:
        return redirect('/')

def wishListView(request):
    wishlistItem = addWishlistedModel.objects.filter(user = request.user.id)
    cartLen = 0
    wishLen = 0
    wishLen+= len(wishlistItem)
    cartItem = addCartModel.objects.filter(user = request.user.id)
    cartLen += len(cartItem)
    try:
        user_profile = UserProfile.objects.get(user = request.user.id)
    except UserProfile.DoesNotExist:
        user_profile = None
    context = {
        'wishlistItem':wishlistItem,
        'cartlen': cartLen,
        'wishlen':wishLen,
        'user_profile':user_profile
    }

    return render(request, 'learningPage.html', context)

def searchResultViews(request):
    query = request.GET.get('search', '')
    sort = request.GET.get('sort', '')
    
    search_results = []
    if query:
        search_results = publishCourse.objects.filter(
            Q(landing_page__title__icontains= query)  |
            Q(landing_page__course_description__icontains = query) |
            Q(course__category__category_name__icontains= query) | 
            Q(course__instructor__user__first_name__icontains = query)  , admin_aprove= True   
        )
    
    if sort:
        if sort == 'most_reviewed':
            courses = publishCourse.objects.filter(admin_aprove= True).annotate(
                review_count=Count('reviews')
            ).order_by('-review_count')
            search_results = courses
        else:
            courses = publishCourse.objects.filter(admin_aprove= True ).order_by('-id')
            search_results = courses
            
    
    wishlistItem = addWishlistedModel.objects.filter(user = request.user.id)
    cartLen = 0
    wishLen = 0
    wishLen+= len(wishlistItem)
    cartItem = addCartModel.objects.filter(user = request.user.id)
    cartLen += len(cartItem)
    try:
        user_profile = UserProfile.objects.get(user = request.user.id)
    except UserProfile.DoesNotExist:
        user_profile = None
    context = {
        'wishlistItem':wishlistItem,
        'cartlen': cartLen,
        'wishlen':wishLen,
        'user_profile':user_profile,
        'search_results': search_results,
        'query': query,
        'len': len(search_results)
    }
    return render(request, 'allCourse.html', context)