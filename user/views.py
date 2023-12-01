from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse, HttpResponseBadRequest
from django.views.decorators.http import require_http_methods
from . import models
from datetime import datetime
from django.db import IntegrityError
from .user_info_retriever import UserInfoRetriever
import uuid

@require_http_methods(["GET"])   
def user(request):
    template = loader.get_template('index.html')
    return HttpResponse(template.render(request=request))

@require_http_methods(["GET"])   
def login(request):
    template = loader.get_template('login.html')
    return HttpResponse(template.render(request=request))

@require_http_methods(["POST"])
def details(request):
    email_address = request.POST.get('email_address')
    password = request.POST.get('password')
    try:
        user = models.User.objects.get(email=email_address)
        if user.password != password:
            raise models.User.DoesNotExist("username and password does not match!")
        user.last_sign_up_date = datetime.now()
        user.save()
        user_info_retriever = UserInfoRetriever(user)
        students = user_info_retriever.get_students_by_parents()
        for s in students:
            print(s)
    except models.User.DoesNotExist:
        template = loader.get_template('not_found.html')
        return HttpResponse(template.render(request=request, context={'email_address': email_address}))
    template = loader.get_template('details.html')
    return HttpResponse(template.render(request=request))

@require_http_methods(["GET"])
def sign_up(request):
    template = loader.get_template('signup.html')
    return HttpResponse(template.render(request=request))

@require_http_methods(["POST"])
def sign_up_confirmation(request):
    email_address = request.POST.get('email')
    if email_address is None or email_address == '':
        return HttpResponseBadRequest("Invalid user email!")
    # TODO(lu): Validate these fields. The basic format and value
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
        template = loader.get_template('signup_confirmation.html', context={'email_address': email_address})
        new_user.save()
        return HttpResponse(template.render(request=request))
    except IntegrityError:
        template = loader.get_template('user_already_exist.html')
        return HttpResponse(template.render({'email_address': email_address}, request=request))

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

@require_http_methods(["GET"])
def reset_password(request):
    template = loader.get_template('reset_password.html')
    return HttpResponse(template.render(request=request))

@require_http_methods(["POST"])
def password_reset_confirmation(request):
   user_email = request.POST.get('email_address')
   if user_email is None or user_email == '':
       return HttpResponseBadRequest("No email address is provided!")
   old_password = request.POST.get('old_password')
   if old_password is None or old_password == '':
       return HttpResponseBadRequest("Invalid old password!")
   new_password = request.POST.get("new_password")
   if new_password is None or new_password == '':
       return HttpResponseBadRequest("Invalid new password!")
   try:
        user = models.User.objects.get(email=user_email)
        if user.password != old_password:
            return HttpResponseBadRequest("Incorrect password is provided!")
        user.password = new_password
        user.save()
   except models.User.DoesNotExist:
        template = loader.get_template('not_found.html')
        return HttpResponse(template.render({'email_address': user_email}))
   template = loader.get_template('details.html')
   return HttpResponse(template.render())

# add a student to a course
@require_http_methods(["POST"])
def add_student(request):
    pass

# Remove a student from a course
@require_http_methods(["POST"])
def remove_student(request):
    pass
