import json
import base64
import os
import time
import boto3

AWS_REGION = os.getenv("AWS_REGION")
SQS_QUEUE_URL = os.getenv("SQS_QUEUE_URL")

if not AWS_REGION or not SQS_QUEUE_URL:
    raise EnvironmentError(
        "AWS_REGION and SQS_QUEUE_URL environment variables must be set"
    )

sqs = boto3.client("sqs", region_name=AWS_REGION)


def publish_message(message: dict):
    payload = json.dumps(message)
    encoded_payload = base64.b64encode(payload.encode("utf-8")).decode("utf-8")

    response = sqs.send_message(
        QueueUrl=SQS_QUEUE_URL,
        MessageBody=encoded_payload
    )

    print(f"Message sent. MessageId: {response['MessageId']}")


if __name__ == "__main__":
    with open("sample_texts.json", "r", encoding="utf-8") as f:
        messages = json.load(f)

    for msg in messages:
        publish_message(msg)
        time.sleep(1)  # small delay to simulate real-time streaming
