from django.db import models
from django.contrib.auth.models import User

"""
Represent the account type of the registered user.
"""
class Member(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    phone_number = models.IntegerField(null=True)
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
    ]
    member_type = models.CharField(max_length=1, choices=MEMBER_TYPE, null=True)

    def __str__(self):
        return 'User Id: {user_id}\n Member type: {member_type}'.format(
            user_id=self.user_id, member_type=self.member_type)

# A user might have multiple students. User must add each student
# explicit to their user profile.

class Student(models.Model):
    parent_id = models.ForeignKey('members.Member', on_delete=models.CASCADE)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    middle_name = models.CharField(max_length=255, null=True)
    GENDER_INFO = [
        ('M', 'Male'),
        ('F', 'Femail'),
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
    class_name = models.CharField(max_length=255)
    school_year = models.DateField(null=False)
    students = models.ManyToManyField(Student, through="Registration")
    course_description = models.CharField(max_length = 255)
    COURSE_TYPE = [
        ('L', 'Language'),
        ('E', 'Enrichment')
    ]
    course_type = models.CharField(max_length=1, choices=COURSE_TYPE)

# Capture the registration event for each student
class Registration(models.Model):
    # unique identifier to the registration. This code will be sent to the user too.
    confirmation_code = models.CharField(max_length=255, primary_key=True)
    school_year = models.DateField(null=False)
    course_id = models.ForeignKey('Course', on_delete=models.CASCADE)
    student = models.ForeignKey('Student', on_delete=models.CASCADE)
    # user = models.ForeignKey('sbccl_webapp.commons.User', on_delete=models.CASCADE)
    registration_date = models.DateField(null=False)
    # TODO(lu): need to consider un-registration/transfer.

# Payment history
class Payment(models.Model):
    registration_code = models.ForeignKey(
        'Registration', on_delete=models.CASCADE, verbose_name='Related registration')
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




