
from members.models import Member, User, Course

from .calender_utils import *
from django.core.mail import EmailMessage, mail_admins

class NotificationUtils(object):
    
    # Find all parent's email information from all active courses in 
    def __get_all_parents():
        start, end = find_current_school_year()
        active_courses = Course.objects.filter(course_type='L',
                                               course_status='A',
                                               school_year_start=start,
                                               school_year_end=end)
        all_parent_emails = set()
        for c in active_courses:
            for student in c.students.all():
                all_parent_emails.add(student.parent_id.user_id.email)
        return all_parent_emails
    
    def __get_all_teachers():
        start, end = find_current_school_year()
        active_courses = Course.objects.filter(course_type='L',
                                        course_status='A',
                                        school_year_start=start,
                                        school_year_end=end)
        all_teacher_emails = set()
        for c in active_courses:
            for student in c.students.all():
                all_teacher_emails.add(student.parent_id.user_id.email)
        return all_teacher_emails
    
    def __get_all_parent_per_class(course_id):
        course = Course.objects.get(id=course_id)
        print('matched course:', course)
        all_parent_emails = set()
        for student in course.students.all():
            all_parent_emails.add(student.parent_id.user_id.email)
        return all_parent_emails 


    # Determines if the member can send notification.
    def can_send_notification(member : Member):
        return member.member_type() in ('T', 'B')
    
    def parse_notification_request(request: dict):
        if 'broadcast' in request and request['broadcast'] != 'None':
            if 'recipient' in request and request['recipient'] != -1:
                raise ValueError("Invalid request: can not accpet more than one recipients!")
            else:
                if request['broadcast'] == 'AllParent':
                    return NotificationUtils.__get_all_parents()
                elif request['broadcast'] == 'AllTeacher':
                    return NotificationUtils.__get_all_teachers()
                else:
                    # Does not support yet.
                    print("Unsupported notification mode %s".format(request['broadcast']))
                    return []
        if 'recipient' not in request or request['recipient'] == -1:
            raise ValueError("Invalid request: No recipient is specified!")
        return NotificationUtils.__get_all_parent_per_class(request['recipient'])

    def notify(sender : User, message):
        all_receivers = NotificationUtils.parse_notification_request(message)
        subject = message['subject']
        if len(subject) <=0:
            raise ValueError("Invalid request: No subject is provided in the email!")
        body = message['body']
        if len(body) <=0:
            raise ValueError("Invalid request: No email body is provided!")
        cced = set()
        if 'cced' in message:
            cced = set(message['cced'])
        cced.add(sender.email) 
        
        email = EmailMessage(
            subject,
            body,
            from_email = "no-reply@sbcclny.com",
            cc = list(cced),
            bcc = list(all_receivers),
            headers={"Message-ID": "Notification"},
        )
        # Failed to send email
        if email.send(fail_silently=False) != 1:
            print("Failed to send group notification!")
            mail_admins(subject="Failed to send to send notifidcation - " + subject,
                        message=body, fail_silently=False)
