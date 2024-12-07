from django.db import models
from django.contrib.auth.models import User

# Coupon will be applied to registration fee. For each purchase, ONLY one coupon can be applied.
class Coupon(models.Model):
    REASON = [
        ('EB', 'EARLY_BIRD'),
        ('BM', 'BOARD_MEMBER')
    ]
    reason = models.CharField(max_length=2, choices=REASON)

    APPLICATION_RULE = [
        ('PR', 'PER_REGISTRATION'),
        ('PA', 'PER_ACCOUNT')
    ]
    application_rule = models.CharField(max_length=2, choices=APPLICATION_RULE)

    TYPE = [
        ('P', 'PERCENTAGE'),
        ('A', 'AMOUNT')
    ]
    type = models.CharField(max_length=1, choices=TYPE)
    # Only valid if the type=A
    dollar_amount = models.FloatField(null=True)

    # Only valid if the type=P. Valid value is between 0 - 100
    # NOTE: percentage type coupon is not supported yet. Don't USE it.
    percentage = models.FloatField(null=True, blank=True)
    expiration_date = models.DateField(null=False)
    creation_date = models.DateField(null=False)
    creator = models.CharField(null=False)

    # unique code that identify this coupon.
    code = models.CharField(max_length=255, default='CCL_EARLY_BIRD')

    def __str__(self):
        reason = 'Early Bird' if self.reason == 'EB' else 'Board member'
        if self.type == 'P':
            return 'Reason: {reason}, Percentage: {percentage}%, Expiration Date: {expiration_date}, Rule: {rule}'.format(
            reason=reason, percentage=self.percentage, expiration_date=self.expiration_date,
            rule=self.application_rule)
        elif self.type == "A":
            return 'Reason: {reason}, Amount: ${amount}, Expiration Date: {expiration_date}, Rule: {rule}'.format(
            reason=reason, amount=self.dollar_amount, expiration_date=self.expiration_date,
            rule=self.application_rule)
        return 'Reason: {reason} Expiration Date: {expiration_date}, Rule: {rule}'.format(
            reason=reason, expiration_date=self.expiration_date, rule=self.application_rule)

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
    verification_code = models.CharField(max_length=255, null=True, blank=True)

    MEMBER_TYPE = [
        ('P', 'Parent'),
        ('B', 'BoardMember'),
        ('V', 'Volunteer'),
        ('T', 'Teacher')
    ]
    member_type = models.CharField(max_length=1, choices=MEMBER_TYPE, null=True)

    # The lastest date that the user signed the CCL terms. This is required for
    # annual registration. Null means the user never sign the term. Every year before
    # school starts, user muse agree to 
    term_signed_date = models.DateField(null=True)

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
    middle_name = models.CharField(max_length=255, null=True, blank=True)
    GENDER_INFO = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('U', 'Unknown')]
    gender = models.CharField(max_length=1, choices=GENDER_INFO)
    date_of_birth = models.DateField(null=True)
    # include both first and last name.
    chinese_name = models.CharField(max_length=255, null=True, blank=True)
    joined_date = models.DateField(null=True, blank=True)
    
    def __str__(self):
        return 'First name: {first_name}\n Last name: {last_name}'.format(
            first_name=self.first_name, last_name=self.last_name)

class InstructorAssignment(models.Model):
    school_year_start = models.DateField(null=False)
    school_year_end = models.DateField(null=False)
    # Course should not be deleted if there is any registration tied to it.
    course = models.ForeignKey('Course', on_delete=models.PROTECT)
    # needs to remove the InstructorAssignment before delete the teacher (member).
    instructor = models.ForeignKey('Member', on_delete=models.PROTECT)
    # The date that this instructor is assigned to the course
    assigned_date = models.DateField(null=False)
    # The date that this assignment expires. Usually this should be the last date of the school year.
    expiration_date = models.DateField(null=True)
    # The assignment could be updated if the teacher left or changed to different class.
    last_update_date = models.DateField(null=True)
    # The person who made the update to this assignment.
    last_update_person = models.CharField(max_length=255, null=False)

    def __str__(self):
        return 'Instructor: {name} Course: {course} School Year: {school_year_start} - {school_year_end}'.format(
            name=self.instructor.user_id, course=self.course.name,
            school_year_start=self.school_year_start.year, school_year_end=self.school_year_end.year)

class Course(models.Model):
    name = models.CharField(max_length=255)
    students = models.ManyToManyField(Student, through="Registration")
    course_description = models.CharField(max_length=1024, blank=True)
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
    # cost for the course. This not does not include the book cost.
    last_update_person = models.CharField(max_length=255, null=False)
    # classroom assignment to this course.
    classroom = models.CharField(max_length=255, null=True, default="Unassigned")
    # One course could be taught by more than one teacher (enrichment). A teach could teach more than
    # one course (Morning and afternoong sessions for the same grade). So this should be a manytomany
    # relationship.
    instructor = models.ManyToManyField(Member, through="InstructorAssignment")
    # When the course starts and ends.
    course_start_time = models.TimeField(null=True)
    course_end_time = models.TimeField(null=True)
    # The cost of the textbook.
    book_cost = models.FloatField(null=True, default=0)
    school_year_start = models.IntegerField(null=False, default=2024)
    school_year_end = models.IntegerField(null=False, default=2025)
    available_date = models.DateField(null=True)

    def __str__(self):
        return 'Course: {name} Course Type: {course_type} Status: {course_status} School Year: {year}'.format(
            name=self.name, course_type=self.course_type, course_status=self.course_status,
            year='-'.join([str(self.school_year_start), str(self.school_year_end)]))

"""
Record the usage of coupons by each member/user.
"""
class CouponUsageRecord(models.Model):
    user = models.ForeignKey(Member, on_delete=models.CASCADE)
    registration = models.ForeignKey('Registration', on_delete=models.CASCADE)
    coupon = models.ForeignKey(Coupon, on_delete=models.PROTECT)
    # The date that this coupon is used
    used_date = models.DateField(null=False)


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
    on_waiting_list = models.BooleanField(null=False, default=False)
    coupons = models.ManyToManyField(Coupon, through='CouponUsageRecord')
    # whether the registration also order textbook
    textbook_ordered = models.BooleanField(null=True, default=False)

    def __str__(self):
        return 'student: {name} course: {course_name} registration code: {registration_code}'.format(
            name=self.student.last_name + ' ' + self.student.first_name,
            course_name=self.course.name, registration_code=self.registration_code)

# Payment history
class Payment(models.Model):
    # Either registration_code or droput_info is null. They can not be set at the same time.
    registration_code = models.ForeignKey(
        'Registration', on_delete=models.SET_NULL, verbose_name='Related registration', null=True, blank=True)
    dropout_info = models.ForeignKey('Dropout', on_delete=models.SET_NULL, verbose_name='Related dropout', null=True, blank=True)
    user = models.ForeignKey(Member, on_delete=models.CASCADE, verbose_name='Payment sender')
    pay_date = models.DateField(null=False)
    original_amount = models.FloatField(null=False)
    amount_in_dollar = models.FloatField(null=False)
    PAYMENT_METHOD = [
        ('NA', 'NOT_AVAILABLE'), # Not paid, hence not set yet
        ('CA', 'CASH'),
        ('CH', 'Check'),
        ('EL', 'Electronic')]
    payment_method = models.CharField(max_length=2, choices=PAYMENT_METHOD, default='NA')
    PAYMENT_STATUS = [
        ('FP', 'FullPayment'),
        ('PP', 'PartialPayment'),
        ('FR', 'FullRefund'),
        ('PR', 'PartialRefund'),
        ('NP', 'NotPaid')
    ]
    payment_status = models.CharField(max_length=2, choices=PAYMENT_STATUS, default='NP')
    last_udpate_date = models.DateField(null=False)
    last_update_person = models.CharField(max_length=255, null=False)

    def __str__(self):
        username = self.user.user_id
        registration_info = ""
        if self.registration_code:
            student_info = self.registration_code.student.last_name + ' ' + self.registration_code.student.first_name
            registration_code = self.registration_code.registration_code
            registration_info = 'student: {student_info} code: {registration_code}'.format(
                student_info=student_info,
                registration_code = registration_code
            )
        else:
            if self.dropout_info:
                student_info = self.dropout_info.student.last_name + ' ' + self.dropout_info.student.first_name
                registration_code = self.dropout_info.original_registration_code
        return 'User: {username} Registration: {registration}'.format(username=username, registration=registration_info)

# If a registration is cancelled, it would become a dropout record.
class Dropout(models.Model):
    school_year_start = models.DateField(null=False)
    school_year_end = models.DateField(null=False)
    course_name = models.CharField(max_length=255, null=False)
    student = models.ForeignKey('Student', on_delete=models.CASCADE)
    original_registration_code = models.CharField(max_length=225)
    dropout_date = models.DateField(null=False)
    user = models.ForeignKey('members.Member', on_delete=models.CASCADE, verbose_name='Dropout requester')

# A group for each class
class ClassGroup(models.Model):
    # a google group will be created with the same name, name@sbcclny.com
    name = models.CharField(max_length=255, null=False)
    # delete the class group first before deleting the course
    course = models.ForeignKey(Course, on_delete=models.PROTECT)
    creation_date = models.DateField(null=False)
    last_update_date = models.DateField(null=False)
    last_update_person = models.CharField(max_length=255, null=False)

class SchoolCalendar(models.Model):
    # School event that happen on that day. If no event, then it can be null.
    event = models.CharField(max_length=255, null=True, db_comment="Event name")
    date = models.DateField(null=False)
    school_year_start = models.IntegerField(null=False)
    school_year_end = models.IntegerField(null=False)
    creation_date = models.DateField(null=False)
    last_update_date = models.DateField(null=False)
    last_update_person = models.CharField(max_length=255, null=False)
    DAY_TYPE = [
        ('SD', 'School Day'),  # Normal school day
        ('HD', 'Holiday'), # Holiday. school is closed
        ('OE', 'Offsite event')]  # off site event, no school
    day_type = models.CharField(max_length=2, choices=DAY_TYPE)

    def getType(self):
        if self.day_type == 'SD':
            return "School Day"
        elif self.day_type == 'HD':
            return "Holiday. School is closed"
        elif self.day_type == 'OE':
            return "Offsite event. No class"
        else:
            return "Unknown day type!"
    
    def __str__(self):
        return '{start}-{end} date: {date} event: {event} type: {day_type}'.format(
            start=self.school_year_start, end=self.school_year_end,
            date=self.date, event=self.event, day_type=self.getType())

    

