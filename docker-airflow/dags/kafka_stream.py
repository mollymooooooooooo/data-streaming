from datetime import datetime
from airflow import DAG
from airflow.operators.python_operator import PythonOperator

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2025, 3, 6),
}

def get_data():
    import requests

    response = requests.get('https://randomuser.me/api/')
    response_json = response.json()
    response_json = response_json['results'][0]
    return response_json

def format_data(response_json):
    data = {}
    location = response_json['location']
    data['first_name'] = response_json['name']['first']
    data['last_name'] = response_json['name']['last']
    data['gender'] = response_json['gender']
    data['address'] = f"{str(location['street']['number'])} {location['street']['name']}"\
        f"{location['city']}, {location['state']}, {location['country']}"
    data['postcode'] = location['postcode']
    data['email'] = response_json['email']
    data['username'] = response_json['login']['username']
    data['dob'] = response_json['dob']['date']
    data['registered_date'] = response_json['registered']['date']
    data['phone'] = response_json['phone']
    data['picture'] = response_json['picture']['medium']
    return data

def stream_data():
    import json
    from kafka import KafkaProducer
    import time
    import logging
   
    # print(json.dumps(res, indent=3))

    producer = KafkaProducer(bootstrap_servers=['broker:29092'], max_block_ms=5000)
    curr_time = time.time()

    while True:
        if time.time() > curr_time + 60:
            break
        try:
             res = get_data()
             res = format_data(res)
             producer.send('users_created', json.dumps(res).encode('utf-8'))
        except Exception as e:
                logging.error(f"An error occurred: {e}")
                continue


with DAG('user_automation', default_args=default_args, schedule_interval='@daily', catchup=False) as dag:

    streaming_task = PythonOperator(
        task_id = 'stream_data_from_api',
        python_callable = stream_data
        )
    
    streaming_task
