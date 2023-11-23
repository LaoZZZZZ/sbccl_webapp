from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse, HttpResponseBadRequest
from django.views.decorators.http import require_http_methods
from . import models
from datetime import datetime
from django.db import IntegrityError
import uuid

@require_http_methods(["GET"])   
def login(request):
    template = loader.get_template('login.html')
    return HttpResponse(template.render())

@require_http_methods(["GET"])
def details(request):
    email_address = request.GET.get('email_address')
    password = request.GET.get('password')
    try:
        user = models.User.objects.get(email=email_address)
        if user.password != password:
            raise models.User.DoesNotExist("username and password does not match!")
        user.last_sign_up_date = datetime.now()
        user.save()
    except models.User.DoesNotExist:
        template = loader.get_template('not_found.html')
        return HttpResponse(template.render({'email_address': email_address}))
    template = loader.get_template('details.html')
    return HttpResponse(template.render())

@require_http_methods(["GET"])
def sign_up(request):
    template = loader.get_template('signup.html')
    print(request)
    return HttpResponse(template.render(request=request))

@require_http_methods(["POST"])
def sign_up_confirmation(request):
    email_address = request.POST.get('email')
    if email_address is None or email_address == '':
        return HttpResponse()
    # TODO(lu): Validate these fields. The basic format and 
    first_name = request.POST.get("first_name")
    last_name = request.POST.get("last_name")
    middle_name = request.POST.get("middle_name")
    phone_number = request.POST.get("phone_number")
    password = request.POST.get("password")
    registration_code = str(uuid.uuid5(uuid.NAMESPACE_URL, email_address))
    join_date = datetime.now()
    try:
        new_user = models.User.objects.create(
            email=email_address,
            first_name=first_name,
            last_name=last_name,
            middle_name=middle_name,
            joined_date=join_date,
            sign_up_status='S',  # still need verification
            verification_code=registration_code,
            password=password,
            phone_number=phone_number)
        new_user.save()
    except IntegrityError:
        template = loader.get_template('user_already_exist.html')
        return HttpResponse(template.render({'email_address': email_address}, request=request))
    template = loader.get_template('signup_confirmation.html', email_address=email_address)
    return HttpResponse(template.render(request=request))

@require_http_methods(["POST"])
def verify_user(request):
    verification_code = request.POST.get('verification_code')
    try:
        user = models.User.objects.get(verification_code=verification_code)
        user.sign_up_status = 'V'
        user.last_sign_up_date = datetime.now()
        user.save()
    except models.User.DoesNotExist:
        template = loader.get_template('not_found.html')
        return HttpResponse(template.render({'verification_code': verification_code}))
    template = loader.get_template('details.html')
    return HttpResponse(template.render())

# TODO(Lu): Fill in the implementation
@require_http_methods(["POST"])
def reset_password(request, user_name, recovery_email):
    pass

# Add a student 
def add_student(request, student_info):
    pass

# add a student to a course
def register_student(request, student_id, course_id):
    pass

# Remove a student from a course
def unregister_student(request, student_id, course_id):
    pass
