from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse
from . import models
   
def login(request):
    template = loader.get_template('login.html')
    return HttpResponse(template.render())

def details(request, user_name, password):
    user = models.User.objects.get(user_name=user_name)
    if user is None:
        return HttpResponse()
    if user.password != password:
        template = loader.get_template('not_found.html')
        return HttpResponse()
    students = models.
    template = loader.get_template('details.html')
    return HttpResponse(template.render())

# TODO(Lu): Fill in the implementation
def sign_up(request, user_name, password):
    pass

# TODO(Lu): Fill in the implementation
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