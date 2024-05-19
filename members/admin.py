from django.contrib import admin
from .models import Member, Registration, Student, Course, Payment, InstructorAssignment, Dropout, Coupon, SchoolCalendar
from django.contrib.auth.models import User

class MemberAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'phone_number',  'member_type', 'sign_up_status')

class StudentAdmin(admin.ModelAdmin):
    list_display = ('first_name', "last_name", 'gender', 'joined_date')

class CourseAdmin(admin.ModelAdmin):
    list_display = ('name', 'course_description', 'course_type', 'course_status', 'size_limit',
                    'classroom', 'course_start_time', 'course_end_time', 'cost', 'book_cost')

class PaymentAdmin(admin.ModelAdmin):
    list_display = ('pay_date', 'registration_code', 'dropout_info', 'original_amount',
                    'amount_in_dollar', 'payment_status')

class RegistrationAdmin(admin.ModelAdmin):
    list_display = ('student', 'course', 'school_year_start', 'school_year_end', 'registration_code',
                    'registration_date', 'expiration_date', 'on_waiting_list', 'textbook_ordered')

class DropoutAdmin(admin.ModelAdmin):
    list_display = ('student', 'course_name', 'school_year_start', 'school_year_end',
                    'original_registration_code', 'dropout_date')

class InstructorAssignmentAdmin(admin.ModelAdmin):
    list_display = ('school_year_start', 'school_year_end', 'course', 'instructor', 'assigned_date',
                    'expiration_date', 'last_update_person', 'last_update_date')
    
class CouponAdmin(admin.ModelAdmin):
    list_disply = ('type', 'reason', 'creation_date', 'expiration_date', 'creator',
                   'last_update_person', 'last_update_date', 'dolloar_amount', 'percentage')

class SchoolCalendarAdmin(admin.ModelAdmin):
    list_disply = ('event', 'date', 'creation_date', 'school_year_start', 'school_year_end',
                   'day_type')


admin.site.register(Member, MemberAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(Payment, PaymentAdmin)
admin.site.register(Registration, RegistrationAdmin)
admin.site.register(InstructorAssignment, InstructorAssignmentAdmin)
admin.site.register(Dropout, DropoutAdmin)
admin.site.register(Coupon, CouponAdmin)
admin.site.register(SchoolCalendar, SchoolCalendarAdmin)

