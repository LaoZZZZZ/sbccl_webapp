
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
    
    def __get_all_parent_per_class(course_id):
        course = Course.objects.get(id=course_id)
        all_parent_emails = set()
        for student in course.students.all():
            all_parent_emails.add(student.parent_id.user_id.email)
        return all_parent_emails 


    # Determines if the member can send notification.
    def can_send_notification(member : Member):
        return member.member_type() in ('T', 'B')
    
    def parse_notification_request(request: dict):
        if 'broadcast' in request:
            if request['recipient'] != -1 and request['broadcast'] != 'None':
                raise ValueError("Invalid request: can not accpet more than one recipients!")
            match request['broadcast']:
                case 'AllParent':
                    return NotificationUtils.__get_all_parents()
                # Does not support yet.
                case ('AllTeacher', 'AllTeachingAssistant'):
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
        print(subject, body, list(all_receivers))
        
        email = EmailMessage(
            subject,
            body,
            from_email = "no-reply@sbcclny.com",
            cc = [sender.email],
            bcc = list(all_receivers),
            headers={"Message-ID": "Notification"},
        )
        # Failed to send email
        if email.send(fail_silently=False) != 1:
            print("Failed to send group notification!")
            mail_admins(subject="Failed to send to send notifidcation - " + subject,
                        message=body, fail_silently=False)