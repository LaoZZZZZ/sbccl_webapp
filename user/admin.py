from django.contrib import admin
from .models import Student, Course, Payment
from django.contrib.auth.models import User

# Register your models here.
class StudentAdmin(admin.ModelAdmin):
    list_display = ('first_name', "last_name", 'gender', 'joined_date')

class CourseAdmin(admin.ModelAdmin):
    list_display = ('class_name', 'school_year', 'course_type')

class PaymentAdmin(admin.ModelAdmin):
    list_display = ('pay_date', 'registration_code', 'original_amount', 'amount_in_dollar', 'PAYMENT_STATUS')

admin.site.register(Student, StudentAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(Payment, PaymentAdmin)