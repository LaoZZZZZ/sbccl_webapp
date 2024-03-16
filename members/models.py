from django.db import models
from django.contrib.auth.models import User

"""
Represent the account type of the registered user.
"""
class Member(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    phone_number = models.CharField(null=True)
    SIGN_UP_STATUS = [
        ('S', 'SignedUp'),
        ('V', 'Verified')
    ]
    sign_up_status = models.CharField(max_length=1, choices=SIGN_UP_STATUS, null=True)
    verification_code = models.CharField(max_length=255, null=True)

    MEMBER_TYPE = [
        ('P', 'Parent'),
        ('B', 'BoardMember'),
        ('V', 'Volunteer'),
        ('T', 'Teacher')
    ]
    member_type = models.CharField(max_length=1, choices=MEMBER_TYPE, null=True)

    def __str__(self):
        return 'User Id: {user_id}\n Member type: {member_type}'.format(
            user_id=self.user_id, member_type=self.member_type)
    
    # Match the MEMBER_TYPE
    def getMemberType(self):
        if self.member_type == 'P':
            return "Parent"
        if self.member_type == 'B':
            return "Board Member"
        if self.member_type == 'V':
            return "Volunteer"
        if self.member_type == 'T':
            return 'Teacher'
        return "Unknown"

# A user might have multiple students. User must add each student
# explicit to their user profile.

class Student(models.Model):
    parent_id = models.ForeignKey('members.Member', on_delete=models.CASCADE)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    middle_name = models.CharField(max_length=255, null=True)
    GENDER_INFO = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('U', 'Unknown')]
    gender = models.CharField(max_length=1, choices=GENDER_INFO)
    date_of_birth = models.DateField(null=True)
    # include both first and last name.
    chinese_name = models.CharField(max_length=255, null=True)
    joined_date = models.DateField(null=True)
    
    def __str__(self):
        return 'First name: {first_name}\n Last name: {last_name}'.format(
            first_name=self.first_name, last_name=self.last_name)

# TODO(lu): Add teacher information.
class Course(models.Model):
    name = models.CharField(max_length=255)
    students = models.ManyToManyField(Student, through="Registration")
    course_description = models.CharField(max_length = 255)
    COURSE_TYPE = [
        ('L', 'Language'),
        ('E', 'Enrichment')
    ]
    course_type = models.CharField(max_length=1, choices=COURSE_TYPE)
    COURSE_STATUS = [
        ('A', 'Active'),  # available for registration
        ('U', 'Unavailable') # not available for registration
    ]
    course_status = models.CharField(max_length=1, choices=COURSE_STATUS)
    size_limit =models.IntegerField(null=False)
    # the date that this course is created.
    creation_date = models.DateField(null=True)
    # the last time that this course was updated
    last_update_time = models.DateField(null=True)
    creater_name = models.CharField(max_length=255, null=False)
    # how much is this course in dollars
    cost = models.FloatField(null=True)
    last_update_person = models.CharField(max_length=255, null=False)

# Capture the registration event for each student
class Registration(models.Model):
    # unique identifier to the registration. This code will be sent to the user too.
    registration_code = models.CharField(max_length=255)
    school_year_start = models.DateField(null=False)
    school_year_end = models.DateField(null=False)
    # Course should not be deleted if there is any registration tied to it.
    course = models.ForeignKey('Course', on_delete=models.PROTECT)
    # needs to remove the registration before delete the students.
    student = models.ForeignKey('Student', on_delete=models.PROTECT)
    registration_date = models.DateField(null=False)
    expiration_date = models.DateField(null=True)
    last_update_date = models.DateField(null=True)

# Payment history
class Payment(models.Model):
    # Either registration_code or droput_info is null. They can not be set at the same time.
    registration_code = models.ForeignKey(
        'Registration', on_delete=models.SET_NULL, verbose_name='Related registration', null=True)
    dropout_info = models.ForeignKey('Dropout', on_delete=models.SET_NULL, verbose_name='Related dropout', null=True)
    user = models.ForeignKey('members.Member', on_delete=models.CASCADE, verbose_name='Payment sender')
    pay_date = models.DateField(null=False)
    original_amount = models.FloatField(null=False)
    amount_in_dollar = models.FloatField(null=False)
    PAYMENT_METHOD = [
        ('CA', 'CASH'),
        ('CH', 'Check'),
        ('EL', 'Electronic')]
    payment_method = models.CharField(max_length=2, choices=PAYMENT_METHOD)
    PAYMENT_STATUS = [
        ('FP', 'FullPayment'),
        ('PP', 'PartialPayment'),
        ('FR', 'FullRefund'),
        ('PR', 'PartialRefund')
    ]
    payment_status = models.CharField(max_length=2, choices=PAYMENT_STATUS)
    last_udpate_date = models.DateField(null=False)
    last_update_person = models.CharField(max_length=255, null=False)

# If a registration is cancelled, it would become a dropout record.
class Dropout(models.Model):
    school_year_start = models.DateField(null=False)
    school_year_end = models.DateField(null=False)
    course_name = models.CharField(max_length=255, null=False)
    student = models.ForeignKey('Student', on_delete=models.CASCADE)
    original_registration_code = models.CharField(max_length=225)
    dropout_date = models.DateField(null=False)
    user = models.ForeignKey('members.Member', on_delete=models.CASCADE, verbose_name='Dropout requester')
