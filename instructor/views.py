from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from instructor.forms import QuestionForm1, QuestionForm2, QuestionForm3
from category.models import Category
from instructor.models import instructorRegister, courseCreateFirstStep, intendedLearner, Module,Video, landingPage, Pricing, welcomeCongratMessages, publishCourse
# Create your views here.
# views.py
from django.contrib import messages
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.encoding import smart_str, force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from PIL import Image
from accounts.models import UserProfile
from learner.models import purchaseCourseModel, reviewCourse
from django.http import JsonResponse
from django.core.mail import send_mail

def instructor_view(request):
    # print(instructorRegister.user)
    if(request.user.is_authenticated) :
        try:
            user = instructorRegister.objects.get(user = request.user)

            try:
                user_profile = UserProfile.objects.get(user = request.user)
            except UserProfile.DoesNotExist:
                user_profile = None

            allCourse = courseCreateFirstStep.objects.filter(instructor__user = request.user)
            return render(request, 'main/course.html', {'allCourse': allCourse, 'user_profile':user_profile})
        except instructorRegister.DoesNotExist:
            return redirect('home')
    else:
        return redirect('home')



def instructorRegisterView(request):
    step = int(request.GET.get('step', 1))
    try:
        user = User.objects.get(username = request.user)

        try:
            instructor = instructorRegister.objects.get(user = user)
            messages.warning(request, "Already Instructed Account Created.")
            return redirect('home')
            
        except instructorRegister.DoesNotExist:
            if request.method == 'POST':
                if step == 1:
                    # Get data from the first step and store it in the session
                    teaching_before = request.POST.get('teaching_before', '')
                    request.session['teaching_before'] = teaching_before
                    print(teaching_before)
                    return redirect(f'/instructor/create/?step=2')  # Redirect to next step
                
                elif step == 2:
                    # Get data from the second step and store it in the session
                    experience = request.POST.get('experience', '')
                    request.session['experience'] = experience
                    return redirect(f'/instructor/create/?step=3')  # Redirect to next step
                
                elif step == 3:
                    # Get data from the third step and store it in the session
                    terms = request.POST.get('terms', '')
                    print(terms)
                    if (terms == ''):
                        messages.error(request, "can't empty terms & conditions.")
                        return redirect(f'/instructor/create/?step=3')
                    request.session['terms'] = terms
                    teaching_before = request.session.get('teaching_before', '')
                    experience = request.session.get('experience', '')
                   
                    if terms:
                        terms = True
                    
                    experience = experience.lower()

                    try:
                        instructorRegister.objects.create(user= user, teaching_before=teaching_before, experience = experience, terms_conditions= terms)
                        user_profile = UserProfile.objects.get(user = user.id)
                        user_profile.instructor = True
                        user_profile.save()
                    except UserProfile.DoesNotExist:
                        messages.error(request, "Return again something error.")
                        return redirect("home")
                    return redirect('instructor') 

        # Retrieve saved data from the session for each step
    except User.DoesNotExist:
        return redirect('login')
    
    teaching_before = request.session.get('teaching_before', '')
    experience = request.session.get('experience', '')
    terms = request.session.get('terms', '')
    


    return render(request, 'question_form.html', { 'step': step, 
                                               'teaching_before' : teaching_before,
                                                'experience':experience,
                                                'terms':terms,
                                                  })


def courseCreate(request):
    step = int(request.GET.get('step', 1))
    category = Category.objects.all()

    if request.user.is_authenticated:
        try: 
            user_ = instructorRegister.objects.get(user = request.user)
            
            if request.method == 'POST':
                    if step == 1:
                        # Get data from the first step and store it in the session
                        title = request.POST.get('title', '')
                        request.session['title'] = title
                        print(title)

                        return redirect(f'/instructor/course/create/?step=2')  # Redirect to next step
                    
                    elif step == 2:
                        # Get data from the second step and store it in the session
                        category_name = request.POST.get('category', '')
                        request.session['category_name'] = category_name
                        return redirect(f'/instructor/course/create/?step=3')  # Redirect to next step
                    
                    elif step == 3:
                        time = request.POST.get('time', '')
                        request.session['time'] = time
                        title = request.session.get('title', '')
                        category_name = request.session.get('category_name', '')
                        time = request.session.get('time', '')
                        if title == '':
                            messages.error(request, "You can't fill title.")
                            return redirect(f'/instructor/course/create/?step=1')
                        if category_name == '':
                            messages.error(request, "You can't choose category.")
                            return redirect(f'/instructor/course/create/?step=2')
                        if time == '':
                            messages.error(request, "You can't choose any option.")
                            return redirect(f'/instructor/course/create/?step=3')
                        
                        instructor = instructorRegister.objects.get(user = request.user)
                        category_ = Category.objects.get(category_name = category_name)
                        user, created = courseCreateFirstStep.objects.get_or_create(instructor = instructor, title = title, category = category_, time= time)
                        uid = urlsafe_base64_encode(force_bytes(user.id))
                        user.uid = uid
                        user.save()
                        Module.objects.create(course = user, title = 'Introduction' )
                    

                        del request.session['title']
                        del request.session['category_name']
                        del request.session['time']

                        return redirect(f'/instructor/course/create/{uid}/intended-learner/') 
        except instructorRegister.DoesNotExist:
            return redirect('home')
    else:      
        return redirect('home')

    title = request.session.get('title', '')
    category_name = request.session.get('category_name', '')
    time = request.session.get('time', '')

    return render(request, 'main/create_course.html', {'category': category, 
                                                       'step':step,
                                                       'title':title,
                                                       'category_name':category_name,
                                                       'time':time,
                                                       })

def descriveCourseCreateView(request, uid):
    print("Hi Abdul ", uid)
    course = courseCreateFirstStep.objects.get(uid = uid)
    return render(request, 'main/descrive_course.html', {'uid': uid, 'course':course})

def courseCurriculum(request, uid):
    if request.user.is_authenticated:
        try:
            user = instructorRegister.objects.get(user = request.user)
            allCourse = (courseCreateFirstStep.objects.filter(instructor = user))
            lst = [i.id for i in allCourse]
            
            if int(smart_str(urlsafe_base64_decode(uid))) in lst:
                course = courseCreateFirstStep.objects.get(uid = uid)
                module, video = None, []

                try: 
                    module = Module.objects.filter(course= course)
                except Module.DoesNotExist:
                    module = None
                cnt = 1
                if request.method == 'POST':
                    addModuleTitle = request.POST.get('add-module-title')
                    if addModuleTitle:
                        Module.objects.create(course = course, title = addModuleTitle)
                        return redirect('curriculum', uid)
                    for i in module:
                        moduleTitle = request.POST.get(f'module-title-{cnt}', '')
                        lectureTitle = request.POST.get(f'lecture-title-{cnt}', '')
                        lectureVideo = request.FILES.get(f'lecture-video-{cnt}', '')
                        # Initialize progress tracking
                        # cache.set('upload_progress', 0)
                        # total_steps = 5

                        # # Simulate file processing steps
                        # for step in range(1, total_steps + 1):
                        #     time.sleep(1)  # Simulate processing time
                        #     progress = int((step / total_steps) * 100)
                        #     cache.set('upload_progress', progress)

                        editCnt = 1
                        editVideo = Video.objects.filter(module = i)
                        for edit in editVideo:
                            editLectureTitle = request.POST.get(f'edit-lectureTitle-{cnt}-{editCnt}')
                            editLectureVideo = request.FILES.get(f'edit-lectureVideo-{cnt}-{editCnt}')
                            editCnt += 1
                            if editLectureTitle:
                                edit.title = editLectureTitle
                                edit.save()
                            if editLectureVideo:
                                edit.video_file = editLectureVideo  
                                edit.save()

                        # print(moduleTitle)
                        if (moduleTitle):
                            i.title = moduleTitle
                            i.save()
                            return redirect('curriculum', uid)
                        if (lectureVideo and lectureTitle):
                            vid = Video(module = i, title = lectureTitle,video_file=lectureVideo)
                            vid.save()
                            # return JsonResponse({'message': 'Upload complete!'})
                            return redirect('curriculum', uid)
                        # else:
                        #     messages.error(request, "Invalid Data provide")
                        #     return redirect('curriculum', uid)
                        cnt += 1

                lst = []
                for i, j  in zip(range(len(module)), module):
                    lst.append(i+1)
                    video_ = Video.objects.filter(module = j)
                    temp = []
                    for k in video_:
                        temp.append(k)
                    video.append(temp)
                module = zip(module, lst)
            else:
                return redirect('home')
        except instructorRegister.DoesNotExist:
            return redirect('home')
    else:
        return redirect('home')
    
    return render(request, 'main/create_course_data/curriculum.html', {"uid": uid, 'module':module, 'video':video, 'course':course})

def lectureDelete(request, uid, lectureId ):
    if request.user.is_authenticated:
        item = get_object_or_404(Video, id = lectureId)
        print(item)
        item.delete()
        messages.success(request, "Lecture delete successfully")
        return redirect('curriculum', uid)
    else:
        redirect('home')

def courseIntendedLernerView(request, uid, pk = None):
    if request.user.is_authenticated:
        try:
            user = instructorRegister.objects.get(user = request.user.id)
            allCourse = (courseCreateFirstStep.objects.filter(instructor = user))
            lst = [i.id for i in allCourse]
            
            if int(smart_str(urlsafe_base64_decode(uid))) in lst:
                course = courseCreateFirstStep.objects.get(uid = uid)
                item = None
                
                try: 
                    item = intendedLearner.objects.get(course= course)
                except intendedLearner.DoesNotExist:
                    item = None
                    
                if request.method == 'POST':
                    student_learn_1 = request.POST.get('student_learn_1', '')
                    student_learn_2 = request.POST.get('student_learn_2', '')
                    student_learn_3 = request.POST.get('student_learn_3', '')
                    student_learn_4 = request.POST.get('student_learn_4', '')
                    course_requirement = request.POST.get('course_requirement', '')
                    who_this_course = request.POST.get('who_this_course', '')
                    if item:
                        item.student_learn_1 = student_learn_1
                        item.student_learn_2 = student_learn_2
                        item.student_learn_3 = student_learn_3
                        item.student_learn_4 = student_learn_4
                        item.course_requirement = course_requirement
                        item.who_this_course = who_this_course
                        messages.success(request, "Successfully updated.")
                    else:
                        
                        item = intendedLearner(course = course, student_learn_1 = student_learn_1, student_learn_2 = student_learn_2, student_learn_3 = student_learn_3, student_learn_4 = student_learn_4,course_requirement =course_requirement,who_this_course = who_this_course  )
                        messages.success(request, "Successfully added.")
                    item.save()
            else:
                return redirect('home')
        except instructorRegister.DoesNotExist:
            return redirect('home')    
    else:
        return redirect('home') 
    return render(request, 'main/create_course_data/intended_lerner.html', {"uid": uid, 'item':item, 'course': course})

def courseLandingPageView(request, uid):
    if request.user.is_authenticated:
        try:
            user = instructorRegister.objects.get(user = request.user)
            allCourse = (courseCreateFirstStep.objects.filter(instructor = user))
            lst = [i.id for i in allCourse]
            
            if int(smart_str(urlsafe_base64_decode(uid))) in lst:
                course = courseCreateFirstStep.objects.get(uid = uid)
                print(course.category.category_name)
            
                try: 
                    item = landingPage.objects.get(course= course)
                except landingPage.DoesNotExist:
                    item = None
                if request.method == 'POST':
                    title = request.POST.get('title', '')
                    course.title = title
                    
                    subtitle = request.POST.get('subtitle', '')
                    description = request.POST.get('description', '')
                    lavel = request.POST.get('lavel', '')
                    category = request.POST.get('category')
                    course_image = request.FILES.get('course_image', '')
                    promotional_video = request.FILES.get('promotional_video', '')
                    if category:
                        categoryName = Category.objects.get(category_name = category)
                        course.category = categoryName
                    else:
                        messages.error(request, "Can't empty category")
                        return redirect('landing_page', uid)
                    if item:
                        item.title = title
                        item.course_subtitle = subtitle
                        item.course_description = description
                        item.level = lavel

                        if course_image:
                            img = Image.open(course_image)
                            width, height = img.size
                            if width != 750 or height != 422:
                                messages.error(request, "Upload specific size image")
                                return redirect('landing_page', uid) 
                            item.coure_image = course_image
                        if promotional_video:
                            item.promotional_video = promotional_video  
                        messages.success(request, "Successfully updated.")         
                    else: 
                        if course_image:
                            img = Image.open(course_image)
                            width, height = img.size
                            if width != 750 or height != 422:
                                messages.error(request, "Upload specific size image")
                                return redirect('landing_page', uid) 
                        item = landingPage(course = course,title = title, course_subtitle = subtitle,  course_description = description, level =lavel,  coure_image =course_image, promotional_video = promotional_video )
                        messages.success(request, "Successfully added.")
                    item.save()
                    print(category, course.category.category_name)
                    course.save()
                category = Category.objects.all()
            else:
                return redirect('home')
        except instructorRegister.DoesNotExist:
            return redirect('home')
    else:
        return redirect('home')
    
    return render(request, 'main/create_course_data/landingPage.html', {"uid": uid, 'item': item, 'course':course, 'category':category})

def coursePricingView(request, uid):
    if request.user.is_authenticated:
        try:
            instructor = instructorRegister.objects.get(user = request.user)
            allCourse = (courseCreateFirstStep.objects.filter(instructor = instructor))
            lst = [i.id for i in allCourse]
            
            if int(smart_str(urlsafe_base64_decode(uid))) in lst:
                course = courseCreateFirstStep.objects.get(uid = uid)
                try: 
                    item = Pricing.objects.get(course= course)
                except Pricing.DoesNotExist:
                    item = None
                if request.method == 'POST':
                    main_price = request.POST.get('main_price', '') 
                    discount = request.POST.get('discount', '')
                    after_discount = 0 
                    if main_price == '':
                        messages.error(request, "Can't empty course price field.")
                        return redirect('pricing', uid)
                    if main_price and discount:
                        after_discount =  str(int(main_price) - (int(main_price) * (int(discount) / 100)))
                    

                    if item:
                        item.main_price = main_price
                        item.discount_percent = discount
                        item.after_discount_price = after_discount
                        messages.success(request, "Successfully updated")
                    else:
                        item = Pricing(course = course, main_price = main_price, discount_percent = discount, after_discount_price  = after_discount)
                        messages.success(request, "Successfully added.")
                    item.save()
                # print(item.after_discount_price)
            else:
                return redirect('home')
        except instructorRegister.DoesNotExist:
            return redirect('home')
    else:
        return redirect('home') 
    return render(request, 'main/create_course_data/pricing.html', {"uid": uid, 'item':item, 'course':course})

def courseMessagesView(request, uid):
    if request.user.is_authenticated:
        try:
            instructor = instructorRegister.objects.get(user = request.user)
            allCourse = (courseCreateFirstStep.objects.filter(instructor = instructor))
            lst = [i.id for i in allCourse]
            
            if int(smart_str(urlsafe_base64_decode(uid))) in lst:
                course = courseCreateFirstStep.objects.get(uid = uid)
                try: 
                    item = welcomeCongratMessages.objects.get(course= course)
                except welcomeCongratMessages.DoesNotExist:
                    item = None
                if request.method == 'POST':
                    welcomeMsg = request.POST.get('welcome_msg', '')
                    congratMsg = request.POST.get('congrat_msg', '')
                    if item:
                        item.welcomeMsg = welcomeMsg
                        item.congratMsg = congratMsg
                        messages.success(request, "Successfully updated")
                    else:
                        item = welcomeCongratMessages(course = course, welcomeMsg = welcomeMsg, congratMsg = congratMsg )
                        messages.success(request, "Successfully added.")
                    item.save()
            else:
                return redirect('home')
        except instructorRegister.DoesNotExist:
            return redirect('home')       
    else:
        return redirect('home')
    return render(request, 'main/create_course_data/messages.html', {"uid": uid, 'item': item, 'course':course})


#  ### Preview course
def previewCourseView(request, uid, slug=None):
    if request.user.is_authenticated:
        try:
            instructor = instructorRegister.objects.get(user=request.user)
            allCourse = (courseCreateFirstStep.objects.filter(instructor = instructor))
            lst = [i.id for i in allCourse]
            
            if int(smart_str(urlsafe_base64_decode(uid))) in lst:
                course = courseCreateFirstStep.objects.get(uid=uid)
                lerner = []
                try:
                    indentend_lerner = intendedLearner.objects.get(course=course)
                    for attr in ['student_learn_1', 'student_learn_2', 'student_learn_3', 'student_learn_4']:
                        value = getattr(indentend_lerner, attr, None)
                        if value:
                            lerner.append(value)
                except intendedLearner.DoesNotExist:
                    lerner = []

                    return redirect('intended_lerner', uid)

                try:
                    pricing = Pricing.objects.get(course=course)
                    module = Module.objects.filter(course=course)
                    landingpage = landingPage.objects.get(course=course)
                    welcomeMsg = welcomeCongratMessages.objects.get(course=course)
                except ( Module.DoesNotExist, landingPage.DoesNotExist, Pricing.DoesNotExist, welcomeCongratMessages.DoesNotExist) as e:
                    if (e.args[0] == 'welcomeCongratMessages matching query does not exist.'):
                        messages.error(request, "Fillup those field.")
                        return redirect('messages', uid)       
                    if (e.args[0] == 'Pricing matching query does not exist.'):
                        messages.error(request, "Fillup those field.")
                        return redirect('pricing', uid)
                    if (e.args[0] == 'landingPage matching query does not exist.'):
                        messages.error(request, "Fillup those field.")
                        return redirect('landing_page', uid)
                    if (e.args[0] == 'Module matching query does not exist.'):
                        messages.error(request, "Fillup those field.")
                        return redirect('curriculum', uid)
                    
                    return redirect('intended_lerner', uid)

                video = []
                video_length = 0
                totalLecture = 0
                if module:
                    for i in module:
                        vide = Video.objects.filter(module=i)
                        temp = []
                        for j in vide:
                            totalLecture += 1
                            temp.append(j.video_file.url)
                            minutes, seconds = map(int, j.duration.split(":"))
                            video_length += minutes + (seconds / 60)
                        video.append(temp)

                temp = video_length
                if temp >= 60:
                    video_length = "%.2f hours" % (temp // 60)
                else:
                    video_length = "%.2f minutes" % temp

                promotional_video = ''
                if slug:
                    try:
                        demo_pro_video = Video.objects.get(slug=slug)
                        promotional_video = demo_pro_video.video_file
                    except Video.DoesNotExist:
                        promotional_video = ''
                elif landingpage:
                    promotional_video = landingpage.promotional_video or ''

                if request.method == 'POST':
                    if len(lerner) < 4 or not (indentend_lerner.course_requirement and indentend_lerner.who_this_course):
                        messages.error(request, "Fill up intended learners data")
                        return redirect('intended_lerner', uid)
                    elif not (landingpage and landingpage.title and landingpage.course_subtitle and landingpage.course_description and landingpage.level and landingpage.coure_image and landingpage.promotional_video):
                        messages.error(request, "Fill up landing page data")
                        return redirect('landing_page', uid)
                    elif not (pricing and pricing.main_price and pricing.discount_percent and pricing.after_discount_price):
                        messages.error(request, "Fill up course pricing data")
                        return redirect('pricing', uid)
                    elif not (welcomeMsg and welcomeMsg.welcomeMsg and welcomeMsg.congratMsg):
                        messages.error(request, "Fill up course messages data")
                        return redirect('messages', uid)

                    # course.publish_true = True
                    # course.save()
                    mail_subject = f'{course.instructor.user.first_name} course approval'
                    
                    recipt_email = ['creative3218@gmail.com',]
                    try:
                        publshcourse = publishCourse.objects.get(course=course)
                        message = f"http://127.0.0.1:8000/admin-course/{publshcourse.slug}/"
                        send_mail(mail_subject, message,'abdulhasib2030@gmail.com', recipt_email)
                        publshcourse.video_length = video_length
                        publshcourse.totalLecture = str(totalLecture)
                        publshcourse.save()
                     
                        if course.publish_true == False:
                            messages.info(request, "Admin approval is pending. Please wait.")
                            return redirect("preview_course", uid)

                        messages.success(request, "Updated successfully.")
                    except publishCourse.DoesNotExist:
                        publshcourse = publishCourse.objects.create(
                            course=course,
                            intended_lerner=indentend_lerner,
                            landing_page=landingpage,
                            pricing=pricing,
                            msg=welcomeMsg,
                            video_length=video_length,
                            totalLecture=str(totalLecture),
                        )
                        
                        message = f"http://127.0.0.1:8000/admin-course/{publshcourse.slug}/"
                        send_mail(mail_subject, message,'abdulhasib2030@gmail.com', recipt_email)
                        messages.success(request, "Your course has been successfully published and is now awaiting admin approval.")
                    return redirect("preview_course", uid)

                context = {
                    "uid": uid,
                    "promotional_video": promotional_video,
                    "title": course.title,
                    "subtitle": landingpage.course_subtitle if landingpage else '',
                    "lerner": lerner,
                    "pricing": pricing,
                    "module": module,
                    "description": landingpage.course_description if landingpage else '',
                    "video": video,
                    "requirement": indentend_lerner.course_requirement,
                    "who_this_course": indentend_lerner.who_this_course if indentend_lerner else '',
                    "video_length": video_length,
                    'course': course,
                }
                return render(request, 'main/create_course_data/previewCourse.html', context)
            else:
                return redirect('home')
        except instructorRegister.DoesNotExist:
            return redirect('home')
    else:
        return redirect('home')



# def course_buyers(request):
#     publish_course = publishCourse.objects.filter(course__instructor__user= request.user)
#     selling_course = purchaseCourseModel.objects.filter(course__in = publish_course)
    
#     try:
#         user_profile = UserProfile.objects.get(user = request.user.id)
#     except UserProfile.DoesNotExist:
#         user_profile = None
#     course_price = []
#     course_review = []
#     for i in selling_course:
#         for j in i.course.all():
#             course_r = reviewCourse.objects.filter(user = i.user, publish_course = j)
#             course_review.append(course_r)
#             dic = {}
#             dic['id'] = j.id
#             dic['price'] = j.pricing.after_discount_price
#             dic['title'] = j.landing_page.title
#             course_price.append(dic)
#     review = []
#     for i in course_review:
#         for j in i: 
#             dic = {}
#             dic['id'] = j.id
#             dic['review_text'] = j.rating_text
#             dic['review_star'] = j.rating_star
#             review.append(dic)
#     print(review)
#     selling_course = zip(selling_course, course_price)
    
#     context = {
#         'user_profile': user_profile,
#         'selling_course': selling_course,
#         'review': review,
#     }
    

#     return render(request, 'main/create_course_data/course_Buyers.html', context)

def showReviewModelInstructor(request, user_id, course_id):
    print(user_id, course_id)
    try:
        review = reviewCourse.objects.get(user = user_id, publish_course=course_id)
    except reviewCourse.DoesNotExist:
        review = None
    data = []
    if review:
        data.append({
            "review_text": review.rating_text,
            "review_star": review.rating_star
        })
    return JsonResponse(data, safe=False)

from instructor.tables import CourseBuyersTable
from learner.models import purchaseCourseModel
from django_tables2 import RequestConfig

def course_buyers(request):
    publish_course = publishCourse.objects.filter(course__instructor__user= request.user)
    selling_course = purchaseCourseModel.objects.filter(course__in = publish_course)
    
    # try:
    #     user_profile = UserProfile.objects.get(user = request.user.id)
    # except UserProfile.DoesNotExist:
    #     user_profile = None
    # course_price = []
    # course_review = []
    # for i in selling_course:
    #     for j in i.course.all():
    #         course_r = reviewCourse.objects.filter(user = i.user, publish_course = j)
    #         course_review.append(course_r)
    #         dic = {}
    #         dic['id'] = j.id
    #         dic['price'] = j.pricing.after_discount_price
    #         dic['title'] = j.landing_page.title
    #         course_price.append(dic)
    # review = []
    # for i in course_review:
    #     for j in i: 
    #         dic = {}
    #         dic['id'] = j.id
    #         dic['review_text'] = j.rating_text
    #         dic['review_star'] = j.rating_star
    #         review.append(dic)
    # print(review)
    # selling_course = zip(selling_course, course_price)
    
    # context = {
    #     'user_profile': user_profile,
    #     'selling_course': selling_course,
    #     'review': review,
    # }
    purchases = purchaseCourseModel.objects.all()
    table = CourseBuyersTable(purchases)

    # Enable pagination (10 items per page)
    RequestConfig(request, paginate={"per_page": 1}).configure(table)
    

    return render(request, 'main/create_course_data/purchase.html', {"table": table})