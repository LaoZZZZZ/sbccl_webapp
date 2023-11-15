from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse
from django.views.decorators.http import require_http_methods
from . import models

@require_http_methods(["GET"])   
def login(request):
    template = loader.get_template('login.html')
    print("handle login request")
    return HttpResponse(template.render())

@require_http_methods(["GET"])
def details(request):
    print("Handling student detail request")
    email_address = request.GET.get('email_address')
    password = request.GET.get('password')
    try:
        user = models.User.objects.get(email=email_address)
        if user.password != password:
            raise models.User.DoesNotExist("username and password does not match!")
    except models.User.DoesNotExist:
        template = loader.get_template('not_found.html')
        return HttpResponse(template.render({'email_address': email_address}))
    template = loader.get_template('details.html')
    return HttpResponse(template.render())

@require_http_methods(["GET"])
def sign_up(request):
    template = loader.get_template('signup.html')
    print("handle signup request")
    return HttpResponse(template.render())

# TODO(Lu): Fill in the implementation
@require_http_methods(["POST"])
def sign_up_confirmation(request):
    template = loader.get_template('signup.html')
    print("handle signup request")
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