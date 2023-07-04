from django.http import HttpResponse
from django.template import loader
from . import models

def board_members(request):
    template = loader.get_template('index.html')
    return HttpResponse(template.render())
   
def login(request):
    template = loader.get_template('login.html')
    return HttpResponse(template.render())

def verify_account(request, user_name, password):
    member = models.BoardMember.objects.get(user_name=user_name)
    if member is None:
        return HttpResponse(loader.get_template('not_found.html'))
    member.account_status = 'V'
    member.save()
    return HttpResponse(loader.get_template('verified.html'))

def details(request, user_name, password):
    member = models.BoardMember.objects.get(user_name=user_name)
    if member is None:
        return HttpResponse(loader.get_template('not_found.html'))
    if member.password != password:
        template = loader.get_template('not_found.html')
        return HttpResponse(loader.get_template('wrong_password.html'))
    
    if member.account_status != 'V':
        return HttpResponse(loader.get_template('verify_account.html'))
    
    return HttpResponse(template.render(loader.get_template('details.html')))

# TODO(Lu): Fill in the implementation
# 1. Reject the request if the user already exists.
# 2. Create an entry in the BoardMember database.
# 3. Send account verification email.
def sign_up(request, user_name, password):
    pass

# TODO(Lu): Fill in the implementation
def reset_password(request, user_name, recovery_email):
    pass

# Add a new course for the school year
def AddCourse(request, class_name, school_year):
    pass

# add a student to a class
def AddStudent(request, student_id, course_id):
    pass

# Update the teacher assignemnt for a course.
def UpdateTeacherForACourse(request, teacher_id, course_id):
    pass