import base64
import json
import logging
import os
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer

# Initialize globally for "Warm Starts" and performance
nltk.download('vader_lexicon', quiet=True)
analyzer = SentimentIntensityAnalyzer()
logger = logging.getLogger(__name__)

def analyze_sentiment(text: str) -> dict:
    """Performs sentiment analysis and returns label/score."""
    if not text or not isinstance(text, str):
        raise ValueError("Input text must be a non-empty string.")
    
    scores = analyzer.polarity_scores(text)
    compound = scores['compound']
    
    if compound >= 0.05:
        label = 'POSITIVE'
    elif compound <= -0.05:
        label = 'NEGATIVE'
    else:
        label = 'NEUTRAL'
    
    return {
        'text': text,
        'sentiment_label': label,
        'sentiment_score': compound
    }

def process_pubsub_message(event, context):
    """Entry point for Google Cloud Function."""
    try:
        if 'data' not in event:
            logger.error("No data found in Pub/Sub message.")
            return

        # Decode and parse message
        message_data = base64.b64decode(event['data']).decode('utf-8')
        message_json = json.loads(message_data)
        text_to_analyze = message_json.get('text')

        if not text_to_analyze:
            logger.warning(f"Payload missing 'text'. Event ID: {context.event_id}")
            return

        # Inference and Logging
        result = analyze_sentiment(text_to_analyze)
        logger.info(f"Result: {json.dumps(result)}")

    except Exception as e:
        logger.error(f"Error: {str(e)}")