import os
import json
import base64
import time
from google.cloud import pubsub_v1

# Configuration via environment variables for security
project_id = os.getenv('GCP_PROJECT_ID')
topic_id = os.getenv('PUB_SUB_TOPIC_ID', 'sentiment-input')
topic_path = f"projects/{project_id}/topics/{topic_id}"

def publish_message(publisher, topic_path, message):
    """Publishes each text entry as a message."""
    data_str = json.dumps(message)
    data_bytes = data_str.encode('utf-8')
    future = publisher.publish(topic_path, data_bytes)
    print(f"Published message ID: {future.result()}")

if __name__ == '__main__':
    if not project_id:
        print("Error: Set GCP_PROJECT_ID environment variable.")
        exit(1)

    publisher_client = pubsub_v1.PublisherClient()
    
    try:
        # Reads from the required sample_texts.json file
        with open('sample_texts.json', 'r', encoding='utf-8') as f:
            sample_texts = json.load(f)
        
        for entry in sample_texts:
            publish_message(publisher_client, topic_path, entry)
            time.sleep(1) # Delay to avoid hitting quotas
            
    except FileNotFoundError:
        print("Error: sample_texts.json not found.")
    except Exception as e:
        print(f"An error occurred: {e}")