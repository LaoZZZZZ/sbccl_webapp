import smtplib, ssl

class EmailSender(object):
    def __init__(self):
        # hard coded smtp servers. We might want to make it configurable.
        # this information is based on
        # https://support.google.com/mail/answer/7126229?visit_id=638239046598120194-2330240748&p=BadCredentials&rd=2#cantsignin&zippy=%2Ci-cant-sign-in-to-my-email-client%2Cstep-change-smtp-other-settings-in-your-email-client
        self.smtp_server = "smtp.gmail.com"
        self.port = 465  # for SSL
        # self.sender_email = "ccl_admin@sbcclny.com"
        self.sender_email = "ccl_admin@sbcclny.com"
        self.password = "Celina@2016"
       
    def SendEmail(self, dest_email, message):
        # Create a secure SSL context
        context = ssl.create_default_context()
        # Try to log in to server and send email
        with smtplib.SMTP_SSL(self.smtp_server, self.port, context=context) as server:
            server.login(self.sender_email, self.password)
            server.sendmail(self.sender_email, dest_email, message)


if __name__ == '__main__':
    message = "Subject: Hi there This message is sent from sbccl."
    email_sender = EmailSender()
    email_sender.SendEmail("luzhao1986@gmail.com", message)