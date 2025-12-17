import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
# MIMEApplication attaching application-specific data (like CSV files) to email messages.
from email.mime.application import MIMEApplication

# Gmail credentials
email_sender = ""
app_password = ""  # The 16-char app password from Google
email_receiver = ""

# Email content
subject = "CyberSec-B6 Test Email from Python "
body = "Hello! test email attachment Regards, Rezwan"
path_to_file = 'test.xlsx'

# Construct email
msg = MIMEMultipart()
msg["From"] = email_sender
msg["To"] = email_receiver
msg["Subject"] = subject
msg.attach(MIMEText(body, "plain"))

# section 1 to attach file
with open(path_to_file,'rb') as file:
    # Attach the file with filename to the email
    msg.attach(MIMEApplication(file.read(), Name="test.xlsx"))

try:
    # Connect to Gmail SMTP server
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()  # Secure the connection
    server.login(email_sender, app_password)
    server.send_message(msg)
    server.quit()

    print("Email sent successfully!")

except Exception as e:
    print("Error:", e)
