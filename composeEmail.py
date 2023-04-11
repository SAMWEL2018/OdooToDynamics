import ssl
import smtplib
from email.message import EmailMessage

class ComposeEmail:

    def SendErrorOnEmail(self,description,message):

        composed = description + message
        self.sender = 'oyakecounter@gmail.com'
        self.passw = 'qhqqtfoepffgxgnk'
        self.receiver = ['wafulasamwel2018@gmail.com', 'john.maina@softiqtechnologies.co.ke',
                         'ombaka@oyake.co.ke', 'purchase@oyake.co.ke',
                         'sales@oyake.co.ke','accounts@oyake.co.ke', 'management@oyake.co.ke']
        # self.receiver = ['wafulasamwel2018@gmail.com']
        self.em = EmailMessage()
        self.em['From'] = self.sender
        self.em['To'] = self.receiver
        self.em['Subject'] = 'Middleware System Error Notification'
        self.em.set_content(composed)

        context = ssl.create_default_context()
        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as conn:
            conn.login(self.sender, self.passw)
            conn.sendmail(self.sender, self.receiver, self.em.as_string())
            print('Email Send !')


