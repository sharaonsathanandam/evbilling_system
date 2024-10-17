import time
import json
from datetime import datetime, timedelta
from kafka import KafkaProducer
from faker import Faker
import random

# Initialize Faker
fake = Faker()

EVENT_HUB_NAMESPACE = 'XXX.servicebus.windows.net:9093'
EVENT_HUB_NAME = 'ev-charging-data'

# Connection string from Event Hubs shared access policies
CONNECTION_STRING = 'Endpoint=sb://XXX.servicebus.windows.net/;SharedAccessKeyName=RootManageSharedAccessKey;SharedAccessKey=XXX'

# Configure the Kafka Producer
producer = KafkaProducer(
    bootstrap_servers=EVENT_HUB_NAMESPACE,
    security_protocol="SASL_SSL",
    sasl_mechanism="PLAIN",
    sasl_plain_username="$ConnectionString",
    sasl_plain_password=CONNECTION_STRING,
    ssl_cafile=None,  # Use default CA certificates
    value_serializer=lambda m: json.dumps(m).encode('utf-8')
)

def generate_ev_data():
    # Generate a unique charger ID (UUID)
    charger_id = fake.uuid4()

    # Generate user contact information
    phone_number = fake.phone_number()
    email = fake.email()

    # Generate start and end times
    start_time = fake.date_time_between(start_date='-1d', end_date='now')
    end_time = start_time + timedelta(minutes=random.randint(15, 120))

    # Calculate duration in minutes
    duration = int((end_time - start_time).total_seconds() / 60)

    # Simulate energy consumed based on duration
    average_consumption_rate = 0.5  # kWh per minute
    energy_consumed = round(duration * average_consumption_rate, 2)

    data = {
        'charger_id': charger_id,
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
        for _ in range(100):  # Send 100 messages
            data = generate_ev_data()
            producer.send(EVENT_HUB_NAME, value=data)
            print(f"Sent: {data}")
            time.sleep(1)  # Wait for a second before sending next message
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        producer.flush()
        producer.close()
