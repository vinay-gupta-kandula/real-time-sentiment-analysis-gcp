# Real-time Sentiment Analysis Pipeline on GCP

## Architecture
Data flows from a local publisher to GCP Pub/Sub, triggering a serverless Cloud Function for inference.

```mermaid
graph LR
    A[publisher.py] --> B(Pub/Sub Topic: sentiment-input)
    B --> C[Cloud Function: analyze_sentiment]
    C --> D[Google Cloud Logging]