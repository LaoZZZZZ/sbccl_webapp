from django.http import HttpResponse
from django.template import loader
from models import Student

def students(request):
    template = loader.get_template('login.html')
    return HttpResponse(template.render())

def single_students(request, user_name, password):
    student = Student.objects.get(user_name=user_name, password=password)
    
