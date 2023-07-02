from django.http import HttpResponse
from django.template import loader
from . import models

def members(request):
    template = loader.get_template('index.html')
    return HttpResponse(template.render())
   
def login(request):
    template = loader.get_template('login.html')
    return HttpResponse(template.render())

def details(request, user_name, password):
    student = models.Student.objects.get(user_name=user_name)
    if student is None:
        return HttpResponse()
    if student.password != password:
        template = loader.get_template('not_found.html')
        return HttpResponse()
    
    template = loader.get_template('details.html')
    return HttpResponse(template.render())

# TODO(Lu): Fill in the implementation
def sign_up(request, user_name, password):
    pass

# TODO(Lu): Fill in the implementation
def reset_password(request, user_name, recovery_email):
    pass
