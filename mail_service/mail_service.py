import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime

from dotenv import load_dotenv
load_dotenv()

def send_mail(links):
    sender = 'newsdigestbysulove@gmail.com'
    receiver = 'bistasulove@gmail.com'
    current_date = f"{datetime.today().strftime('%A, %b %d %Y')}"

    msg = MIMEMultipart('alternative')
    msg['Subject'] = f"News Digest for {current_date}"
    msg['From'] = f"News Digest{sender}"
    msg['To'] = receiver

    html = f"""
        <html>
            <body>
                Hello,
                I hope you're having wonderful day today. As per your request, 
                I have found {len(links.keys())} news that you might interesting to read today. Have fun.
                <ul>
                    {''.join(['<li><a href="'+ value +'">' + key + '</a></li>' for key,value in links.items()])}
                </ul>
                <br></br>
                <p>Made with love by <a href="https://linkedin.com/bistasulove">Sulove Bista</a><p>
            </body>
        </html>
    """
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

