# birtday wisher python script

import smtplib
import datetime as dt
import pandas
import random
from dotenv import load_dotenv
import os

load_dotenv()

birthdays_df = pandas.read_csv("birthdays.csv")

today = dt.datetime.now()

today_month = today.month

today_day = today.day

sun_trip_subjects = [
    "Another Trip Around the Sun!",
    "+1 Trip Around the Sun Completed!",
    "One More Lap Around the Sun!",
    "Successfully Completed Another Orbit!",
    "Round Trip Around the Sun: Done!",
    "+1 Revolution Around the Sun!",
    "Another 365-Day Orbit - Nailed It!",
    "You Just Leveled Up Around the Sun!",
    "Solar Orbit Complete - Happy Birthday!",
    "Another Perfect Trip Around the Sun!",
]

files_list = ["letter_1.txt", "letter_2.txt", "letter_3.txt"]
matching_person = birthdays_df[
    (birthdays_df["month"] == today_month) & (birthdays_df["day"] == today_day)
]

if not matching_person.empty:
    name = matching_person.iloc[0]["name"]  # Takes the correct person
    email = matching_person.iloc[0]["email"]  # Correct email
    # print(name, type(name))

    # choosing random files out of three
    random_file = random.choice(files_list)
    # print(random_file)

    # replacing the [NAME] with actual name
    with open(random_file, "r") as f:
        content = f.read()
        bd_wish = content.replace("[NAME]", name)

    # print(bd_wish, type(bd_wish))

    # getting the subject
    sub = random.choice(sun_trip_subjects)
    final_message = f"Subject: {sub}\n\n{bd_wish}"

    # print(final_message, type(final_message))

    # sending mail
    connection = smtplib.SMTP("smtp.gmail.com", 587)
    connection.starttls()
    connection.login(user=os.getenv("MY_EMAIL"), password=os.getenv("MY_PASSWORD"))

    connection.sendmail(
        from_addr=os.getenv("MY_PASSWORD"), to_addrs=email, msg=f"Subject: {sub}\n\n{bd_wish}"
    )
    connection.close()

else:
    print("No bday today")

# -- Use the Python anywhere to run the code automatically every day at morning 06 AM
