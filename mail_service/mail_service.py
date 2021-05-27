import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from dotenv import load_dotenv
load_dotenv()

def send_mail(links):
    sender = 'newsdigestbysulove@gmail.com'
    receiver = 'bistasulove@gmail.com'

    msg = MIMEMultipart('alternative')
    msg['Subject'] = "Link"
    msg['From'] = sender
    msg['To'] = receiver

    html = """
        <h4> %s links you might be interested in today: </h4>
        %s
    """ % (len(links), '<br></br>').join(links)
    
    mime = MIMEText(html, 'html')

    msg.attach(mime)

    try:
        mail = smtplib.SMTP('smtp.gmail.com', 587)
        mail.ehlo()
        mail.starttls()
        mail.login(sender, os.environ.get('PASSWORD'))
        mail.sendmail(sender, receiver, msg.as_string())
        mail.quit()
    except Exception as e:
        print("Something went wrong while sending mail. Error:", e)

