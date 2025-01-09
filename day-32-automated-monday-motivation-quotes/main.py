import smtplib
import datetime as dt
import random
import time

MY_EMAIL = "youremail@gmail.com"
MY_PASSWORD = "yourapppassword"


def get_quote():
    with open("quotes.txt", "r") as data_file:
        quotes = data_file.readlines()
        quote = random.choice(quotes)
        return quote


def send_email(my_email, my_password):
    retries = 3
    for attempt in range(retries):
        try:
            print(f"Attempt {attempt + 1} to send email")
            with smtplib.SMTP("smtp.gmail.com", 587, timeout=30) as connection:
                connection.starttls()
                connection.login(my_email, my_password)
                connection.sendmail(
                    from_addr=my_email,
                    to_addrs=my_email,
                    msg=f"Subject:Monday Motivation\n\n{get_quote()}"
                )
            print("Email sent successfully")
            break
        except (smtplib.SMTPException, TimeoutError) as e:
            print(f"Failed to send email, attempt {attempt + 1} of {retries}")
            print(f"Error: {e}")
            time.sleep(5)  # wait a little before retrying
    else:
        print("Failed to send email after several attempts")


now = dt.datetime.now()
day_of_week = now.weekday()

if day_of_week == 0:  # Monday
    send_email(MY_EMAIL, MY_PASSWORD)
else:
    print("Today is not Monday")