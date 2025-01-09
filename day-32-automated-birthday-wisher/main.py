import smtplib
import os
import random
import time
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

MY_EMAIL = os.getenv("MY_EMAIL")
MY_PASSWORD = os.getenv("MY_PASSWORD")

def get_quote():
    with open("quotes.txt", "r") as data_file:
        quotes = data_file.readlines()
        return random.choice(quotes)

def send_email(my_email, my_password):
    retries = 3
    for attempt in range(retries):
        try:
            print(f"Attempt {attempt + 1} to send email")
            with smtplib.SMTP("smtp.gmail.com", 587, timeout=30) as connection:
                connection.starttls()
                connection.login(my_email, my_password)

                msg = MIMEMultipart()
                msg['From'] = my_email
                msg['To'] = my_email
                msg['Subject'] = "Monday Motivation"
                msg.attach(MIMEText(get_quote(), 'plain'))

                connection.send_message(msg)
            print("Email sent successfully")
            break
        except smtplib.SMTPAuthenticationError:
            print("Failed to authenticate with the SMTP server. Check your email and password.")
            break
        except smtplib.SMTPConnectError:
            print("Failed to connect to the SMTP server. Check your internet connection.")
            break
        except smtplib.SMTPRecipientsRefused:
            print("The recipient's email address was refused by the server.")
            break
        except (smtplib.SMTPException, TimeoutError) as e:
            print(f"Failed to send email, attempt {attempt + 1} of {retries}")
            print(f"Error: {e}")
            time.sleep(5)  # wait a little before retrying
    else:
        print("Failed to send email after several attempts")