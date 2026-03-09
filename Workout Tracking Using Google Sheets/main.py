# Workout tracking using google sheets

import requests
from datetime import datetime
import re
from dotenv import load_dotenv
import os

load_dotenv()

nea_header = {
    "x-app-id": os.getenv("APP_ID"),
    "x-app-key": os.getenv("NUTRITION_API_KEY"),
}

sheety_header = {
    "Authorization": f"Bearer {os.getenv("BEARER_TOKEN")}"
}

# user_ip example - swam for 1 hour
user_ip = input("Tell me which exercises you did: ")
user_ip_list = None

if 'and' in user_ip and ',' in user_ip:
    user_ip_list = re.split(r',\s*|\s+and\s+', user_ip)
elif 'and' in user_ip:
    user_ip_list = user_ip.split('and')
elif ',' in user_ip:
    user_ip_list = user_ip.split(',')

request_body = {"query": user_ip}

post_endpoint = f"{os.getenv("NUTRITION_EXERCISE_API_ENDPOINT")}//v1/nutrition/natural/exercise"

# getting hold of date and time
today = datetime.now()

date = today.strftime('%d/%m/%Y')
time = today.strftime('%X')


if user_ip_list is not None and len(user_ip_list) >= 2:
    for i in user_ip_list:
        
        request_body = {
            "query": i
        }
        # * nea - NUTRITION EXERCISE API
        nea_response = requests.post(url=post_endpoint, json=request_body, headers=nea_header)

        nea_response.raise_for_status()

        data = nea_response.json()

        print(data)
        
        body = {
        "workout":{
            "date": date,
            "time": time,
            "exercise": data['exercises'][0]['name'].title(),
            "duration": data['exercises'][0]['duration_min'],
            "calories": data['exercises'][0]['nf_calories']
        }
    }

        sheety_response = requests.post(url=os.getenv("SHEETY_ENDPOINT"), json=body, headers=sheety_header)

        sheety_response.raise_for_status()

        sheety_data = sheety_response.json()

        print(sheety_data, sheety_response.text)
else:
    nea_response = requests.post(url=post_endpoint, json=request_body, headers=nea_header)

    nea_response.raise_for_status()

    data = nea_response.json()

    print(data)

    body = {
        "workout":{
            "date": date,
            "time": time,
            "exercise": data['exercises'][0]['name'].title(),
            "duration": data['exercises'][0]['duration_min'],
            "calories": data['exercises'][0]['nf_calories']
        }
    }

    sheety_response = requests.post(url=os.getenv("SHEETY_ENDPOINT"), json=body, headers=sheety_header)

    sheety_response.raise_for_status()

    sheety_data = sheety_response.json()

    print(sheety_data, sheety_response.text)
