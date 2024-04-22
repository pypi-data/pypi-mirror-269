The library newsly_mail allows you to send customized emails in your python project. 

1. Download the package from pip:

pip install newsly-mail

2. Import the send_email function from the library:

from newsly_mail import send_email

3. Send customized emails by calling the send_email function in your code:

send_email(
                sender_email='test@xyz.com',
                receiver_email=user.email,
                subject="Headline",
                body="Mail Body",
                smtp_server='smtp.xyz.com',
                smtp_port=SMTP_PORT,
                smtp_username='test@abc.com',
                smtp_password='*************'
            )
