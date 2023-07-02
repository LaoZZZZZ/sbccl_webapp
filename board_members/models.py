from django.db import models

class BoardMember(models.Model):
    id = models.IntegerField(primary_key=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    middle_name = models.CharField(max_length=255, null=True)
    email = models.CharField(max_length=255)
    recovery_email = models.CharField(max_length=255)
    join_date = models.DateField(null=True)
    password = models.CharField(max_length=255)
    phone_number = models.IntegerField(null=True)
    user_name = models.CharField(max_length=255, null=True)
    GENDER_INFO = [
        ('M', 'Male'),
        ('F', 'Femail'),
        ('U', 'Unknown')]
    gender = models.CharField(max_length=1, choices=GENDER_INFO)
    # include both first and last name.
    chinese_name = models.CharField(max_length=255, null=True)
    JOB_STATUS = [
        ('A', 'Active'),
        ('L', 'Leave'),
        ('U', 'Unknown')
    ]
    job_status = models.CharField(max_length=1, choices=JOB_STATUS)
    # short summary of this board member's responsibility.
    job_description = models.CharField(max_length=255, null=True)

