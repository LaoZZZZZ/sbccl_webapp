from django.core.mail import EmailMessage, send_mail


def SendSignUpConfirmationEmail(verification_code):
    pass

"""
@subject: The subject of the email
@msg: The email body
@receipient_list: A list of email addresses receiver.
@from_email: The send email. None means the sending will use the value of DEFAULT_FROM_EMAIL 
"""
def SendEmails(subject, body, recipient_list, from_email = None):
    send_mail(subject, body, recipient_list, fail_silently=False)