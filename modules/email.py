from email.mime.text import MIMEText
import smtplib

def emailChange(toAddress, fromAddress, emailAppPassword, subject, text):
    try:
        smtp_server = smtplib.SMTP('smtp.gmail.com', 587)
        smtp_server.ehlo()
        smtp_server.starttls()
        smtp_server.login(fromAddress, emailAppPassword)
        # Create email body
        message = MIMEText(text)
        message['From'] = fromAddress
        message['To'] = toAddress
        message['Subject'] = subject
        # Send the email
        smtp_server.sendmail(fromAddress, toAddress, message.as_string())
        smtp_server.quit()
        print('Email sent successfully')
    except Exception as e:
        print("Error: " + e.message)