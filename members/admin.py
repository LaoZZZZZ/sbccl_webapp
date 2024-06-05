from django.contrib import admin
from .models import Member, Registration, Student, Course, Payment, InstructorAssignment, Dropout, Coupon, SchoolCalendar
from django.contrib.auth.models import User

class MemberAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'phone_number',  'member_type', 'sign_up_status')
    search_fields = ['user_id__email', 'phone_number', 'member_type', 'sign_up_status']

class StudentAdmin(admin.ModelAdmin):
    list_display = ('first_name', "last_name", 'gender', 'joined_date')
    search_fields = ['first_name', 'last_name', 'gender']

class CourseAdmin(admin.ModelAdmin):
    list_display = ('name', 'course_description', 'course_type', 'course_status', 'size_limit',
                    'classroom', 'course_start_time', 'course_end_time', 'cost', 'book_cost')
    search_fields = ['name', 'course_type', 'course_status', 'classroom']

class PaymentAdmin(admin.ModelAdmin):
    list_display = ('pay_date', 'registration_code', 'dropout_info', 'original_amount',
                    'amount_in_dollar', 'payment_status', 'payment_method', 'user')
    search_fields = ['payment_status', 'payment_method', 'last_update_person',
                     'registration_code__registration_code', 'user__user_id__email']

class RegistrationAdmin(admin.ModelAdmin):
    list_display = ('student', 'course', 'school_year_start', 'school_year_end', 'registration_code',
                    'registration_date', 'expiration_date', 'on_waiting_list', 'textbook_ordered')
    search_fields = ['registration_code', 'course__name', 'student__first_name', 'student__last_name']

class DropoutAdmin(admin.ModelAdmin):
    list_display = ('student', 'course_name', 'school_year_start', 'school_year_end',
                    'original_registration_code', 'dropout_date')
    search_fields = ['original_registration_code', 'student__first_name', 'student__last_name',
                     'course_name']

class InstructorAssignmentAdmin(admin.ModelAdmin):
    list_display = ('school_year_start', 'school_year_end', 'course', 'instructor', 'assigned_date',
                    'expiration_date', 'last_update_person', 'last_update_date')
    search_fields = ['course__name', 'instructor__user_id__email', 'instructor__user_id__first_name']
    
class CouponAdmin(admin.ModelAdmin):
    list_disply = ('type', 'reason', 'creation_date', 'expiration_date', 'creator',
                   'last_update_person', 'last_update_date', 'dolloar_amount', 'percentage', 'code')
    search_fields = ['creator', 'type', 'reason', 'code']

class SchoolCalendarAdmin(admin.ModelAdmin):
    list_disply = ('event', 'date', 'creation_date', 'school_year_start', 'school_year_end',
                   'day_type')
    search_fields = ['school_year_start', 'school_year_end', 'day_type']


admin.site.register(Member, MemberAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(Payment, PaymentAdmin)
admin.site.register(Registration, RegistrationAdmin)
admin.site.register(InstructorAssignment, InstructorAssignmentAdmin)
admin.site.register(Dropout, DropoutAdmin)
admin.site.register(Coupon, CouponAdmin)
admin.site.register(SchoolCalendar, SchoolCalendarAdmin)

