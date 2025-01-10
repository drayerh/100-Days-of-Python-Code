import requests
from datetime import datetime, timezone
import smtplib
import time
import os
import signal
import sys

# Constants for the latitude and longitude of the location to be monitored
MY_LAT = 51.507351
MY_LONG = -0.127758

# Retrieve email credentials from environment variables
MY_EMAIL = os.getenv("MY_EMAIL")
MY_PASSWORD = os.getenv("MY_PASSWORD")

def overhead_check():
    """
    Check if the ISS is currently overhead within a 5-degree range of the specified location.

    Returns:
        bool: True if the ISS is overhead, False otherwise.
    """
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    data = response.json()

    iss_latitude = float(data["iss_position"]["latitude"])
    iss_longitude = float(data["iss_position"]["longitude"])

    if MY_LAT - 5 <= iss_latitude <= MY_LAT + 5 and MY_LONG - 5 <= iss_longitude <= MY_LONG + 5:
        return True
    return False

def is_night():
    """
    Check if it is currently nighttime at the specified location.

    Returns:
        bool: True if it is nighttime, False otherwise.
    """
    parameters = {
        "lat": MY_LAT,
        "lng": MY_LONG,
        "formatted": 0,
    }
    response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()
    data = response.json()
    sunrise = datetime.fromisoformat(data["results"]["sunrise"]).replace(tzinfo=timezone.utc)
    sunset = datetime.fromisoformat(data["results"]["sunset"]).replace(tzinfo=timezone.utc)

    time_now = datetime.now(timezone.utc)

    if time_now >= sunset or time_now <= sunrise:
        return True
    return False

def send_email():
    """
    Send an email notification indicating that the ISS is overhead.
    """
    with smtplib.SMTP("smtp.gmail.com") as connection:
        connection.starttls()
        connection.login(MY_EMAIL, MY_PASSWORD)
        connection.sendmail(from_addr=MY_EMAIL,
                            to_addrs=MY_EMAIL,
                            msg="Subject: ISS ALERT\n\n Look up, ISS is above you in the sky."
                            )

def signal_handler(sig, frame):
    """
    Handle the SIGINT signal to gracefully exit the script.

    Args:
        sig (int): Signal number.
        frame (FrameType): Current stack frame.
    """
    print('Exiting...')
    sys.exit(0)

# Register the signal handler for SIGINT
signal.signal(signal.SIGINT, signal_handler)

# Main loop to check ISS position and time every 60 seconds
while True:
    time.sleep(60)
    if overhead_check() and is_night():
        send_email()