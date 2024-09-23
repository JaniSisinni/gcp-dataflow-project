from google.cloud import pubsub_v1
import json
import time
import random
import uuid
from datetime import datetime, timedelta

project_id = "gcp-flight-data-project"  
topic_id = "flight-data-topic" 

publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path(project_id, topic_id)

def generate_random_flight_data():
    """
    Generates random flight data.
    """
    flight_id = str(uuid.uuid4())[:8]  
    departure_airport = random.choice(["LAX", "JFK", "SFO", "ORD", "DFW"])  
    arrival_airport = random.choice(["JFK", "SFO", "ORD", "DFW", "MIA"])  
    departure_timestamp = (datetime.now() + timedelta(days=random.randint(0, 30))).isoformat() + 'Z'  
    arrival_timestamp = (datetime.now() + timedelta(days=random.randint(0, 30), hours=random.randint(1, 12))).isoformat() + 'Z' 
    delay_time = random.randint(0, 300)  
    cancelation = random.randint(0, 1)  
    passengers = random.randint(150, 300)  

    return {
        'flight_id': flight_id,
        'departure_airport': departure_airport,
        'arrival_airport': arrival_airport,
        'departure_timestamp': departure_timestamp,
        'arrival_timestamp': arrival_timestamp,
        'delay_time': delay_time,
        'cancelation': cancelation,
        'passengers': passengers
    }

def publish_flight_data():
    """
    Publishes randomly generated flight data to the specified Pub/Sub topic.
    """
    flight_data = generate_random_flight_data()  # Generate random flight data
    
    message = json.dumps(flight_data).encode('utf-8') 
    future = publisher.publish(topic_path, message)  
    print(f"Published message ID: {future.result()}")  

if __name__ == '__main__':
    while True:
        publish_flight_data()  # Publish flight data
        time.sleep(5)  
