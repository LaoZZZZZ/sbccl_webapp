from django.contrib import admin
from .models import Member, Registration, Student, Course, Payment
from django.contrib.auth.models import User

class MemberAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'phone_number',  'member_type', 'sign_up_status')

class StudentAdmin(admin.ModelAdmin):
    list_display = ('first_name', "last_name", 'gender', 'joined_date')

class CourseAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'course_description', 'course_type', 'course_status', 'size_limit')

class PaymentAdmin(admin.ModelAdmin):
    list_display = ('pay_date', 'registration_code', 'original_amount', 'amount_in_dollar', 'PAYMENT_STATUS')

class RegistrationAdmin(admin.ModelAdmin):
    list_display = ('student', 'course', 'school_year', 'registration_code',
                    'registration_date', 'expiration_date')

admin.site.register(Member, MemberAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(Payment, PaymentAdmin)
admin.site.register(Registration, RegistrationAdmin)