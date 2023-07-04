from django.db import models

class User(models.Model):
    # User is uniquely identified by their email.
    email = models.CharField(max_length=255, primary_key=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    middle_name = models.CharField(max_length=255, null=True)
    recovery_email = models.CharField(max_length=255)
    joined_date = models.DateField(null=True)
    password = models.CharField(max_length=255)
    phone_number = models.IntegerField(null=True)
    user_name = models.CharField(max_length=255, null=True)

# A user might have multiple students. User must add each student
# explicit to their user profile.
class Student(models.Model):
    parent_id = models.ForeignKey(User, on_delete=models.CASCADE)
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
    course_id = models.ForeignKey(Course, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    registration_date = models.DateField(null=False)
    # TODO(lu): need to consider un-registration/transfer.

# Payment history
class Payment(models.Model):
    registration_code = models.ForeignKey(Registration, verbose_name='Related registration')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Payment sender')
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



