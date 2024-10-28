import os
import time
import json
from datetime import datetime, timedelta
from kafka import KafkaProducer
from faker import Faker
import random

# Initialize Faker
fake = Faker()

# Retrieve configurations from environment variables
EVENT_HUB_NAMESPACE = os.environ.get('EVENT_HUB_NAMESPACE')
EVENT_HUB_NAME = os.environ.get('EVENT_HUB_NAME')
CONNECTION_STRING = os.environ.get('CONNECTION_STRING')

# Configure the Kafka Producer
producer = KafkaProducer(
    bootstrap_servers=f"{EVENT_HUB_NAMESPACE}",
    security_protocol="SASL_SSL",
    sasl_mechanism="PLAIN",
    sasl_plain_username="$ConnectionString",
    sasl_plain_password=CONNECTION_STRING,
    ssl_cafile=None,  # Use default CA certificates
    value_serializer=lambda m: json.dumps(m).encode('utf-8')
)

# Generate a unique charger ID (UUID)
charger_id = random.randint(1000,9999)

#Declare Charger types:
charger_type={"Level-1":7.2,"Level-2":50,"DCFC1":150,"DCFC2":300}

def generate_ev_data():
    # Generate user contact information
    phone_number = fake.numerify("###-###-####")
    email = fake.email()

    # Generate start and end times
    start_time = fake.date_time_between(start_date='-1d', end_date='now')
    random_charger = random.choice(list(charger_type.items()))
    rand_charger_type = random_charger[0]
    charging_speed = random_charger[1]

    if charging_speed == 7.2:
        end_time = start_time + timedelta(minutes=random.randint(30, 480))
        energy_consumed = random.randint(10,80)
    elif charging_speed == 50:
        end_time = start_time + timedelta(minutes=random.randint(15, 120))
        energy_consumed = random.randint(20, 80)
    elif charging_speed == 150:
        end_time = start_time + timedelta(minutes=random.randint(1, 60))
        energy_consumed = random.randint(10, 80)
    else:
        end_time = start_time + timedelta(minutes=random.randint(1,30 ))
        energy_consumed = random.randint(10, 80)


    # Calculate duration in minutes
    duration = int((end_time - start_time).total_seconds() / 60)

    data = {
        'charger_id': charger_id,
        'charger_type': rand_charger_type,
        'start_time': start_time.isoformat(),
        'end_time': end_time.isoformat(),
        'duration_minutes': duration,
        'energy_consumed': energy_consumed,
        'phone_number': phone_number,
        'email': email
    }
    return data

if __name__ == "__main__":
    try:
        while True:
            data = generate_ev_data()
            producer.send(EVENT_HUB_NAME, value=data)
            print(f"Sent: {data}")
            time.sleep(1)  # Wait for a second before sending the next message
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        producer.flush()
        producer.close()