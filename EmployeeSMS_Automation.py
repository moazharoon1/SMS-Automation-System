import cx_Oracle

import requests

import os

import json

from datetime import datetime

BASE_URL = "https://vjqz6p.api.infobip.com"

API_KEY = "" #YOUR API KEY GOES HERE

STATE_FILE_PATH = "state.json"


def send_sms_via_api(message, recipient):
    print("enter send sms")

    url = f"{BASE_URL}/sms/2/text/advanced"

    headers = {

        "Content-Type": "application/json",

        "Authorization": f"App {API_KEY}",

    }

    payload = {

        "messages": [

            {

                "destinations": [{"to": recipient}],

                "text": message,

            }

        ]

    }

    response = requests.post(url, json=payload, headers=headers)

    print(f"Response status code: {response.status_code}")

    if response.status_code == 200:

        response_data = response.json()

        message_id = response_data["messages"][0]["messageId"]

        print(f"SMS sent successfully. Message ID: {message_id}")

    else:

        print("SMS sending failed.")


def read_sms_to_send():
    print("Inside read_sms_to_send() function")
    print(os.getcwd())

    dsn_tns = cx_Oracle.makedsn(

        "localhost",  # Replace with your Oracle database host

        1522,  # Replace with your Oracle database port (usually 1521) (1522 in my case)

        service_name="ORCL",  # Replace with your Oracle service name

    )

    conn = cx_Oracle.connect(

        user="",  # Replace with your Oracle database user

        password="",  # Replace with your Oracle database password

        dsn=dsn_tns,

    )

    cursor = conn.cursor()

    if cursor:
        print("cursor exists")

    last_execution_time = get_last_execution_time()

    print(f"last execution time: {last_execution_time}")

    select_query = "SELECT DEPARTURE_DATE, RETURN_DATE, MOB FROM VM_TRX_HEADER WHERE STS_UPDATE_TIME IS NOT NULL"
    
    if last_execution_time:
        formatted_last_execution_time = last_execution_time.strftime('%d/%m/%Y %I:%M:%S %p')
        
        select_query += f" AND STS_UPDATE_TIME > TO_TIMESTAMP('{formatted_last_execution_time}', 'DD/MM/YYYY HH:MI:SS AM')"

    print(f"Executing the query: {select_query}")

    cursor.execute(select_query)

    rows = cursor.fetchall()

    print(f"Number of rows fetched: {len(rows)}")

    print(f"Fetched rows: {rows}")

    for departure_date, return_date, mob in rows:
        # You can customize the SMS message body here, e.g., "Hello, Your requested vehicle has been registered to

        # you from {departure_date} to {return_date}."

        message = f"Hello, Your requested vehicle has been registered to you from {departure_date} to {return_date}."

        recipient = ""  # Replace with your recipient's phone number

        send_sms_via_api(message, recipient)

    cursor.close()

    conn.close()

    save_execution_time(datetime.now())


def get_last_execution_time():
    if os.path.exists(STATE_FILE_PATH):

        with open(STATE_FILE_PATH, "r") as state_file:

            state = json.load(state_file)

            last_execution_time = state.get("last_execution_time")

            if last_execution_time:
                # Convert the stored timestamp to a Python datetime object

                formatted_timestamp = datetime.strptime(last_execution_time, '%m/%d/%Y %I:%M:%S %p')

                return formatted_timestamp

    return None


def save_execution_time(timestamp):
    # Convert the timestamp to the format 'MM/DD/YYYY HH:MI:SS.FF AM/PM'

    formatted_timestamp = timestamp.strftime('%d/%m/%Y %I:%M:%S %p')

    state = {"last_execution_time": formatted_timestamp}

    with open(STATE_FILE_PATH, "w") as state_file:
        json.dump(state, state_file)

    print(f"Timestamp saved: {formatted_timestamp}")


if __name__ == "__main__":
    read_sms_to_send()
