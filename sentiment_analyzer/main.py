import json
import base64
import logging
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global Model Initialization
try:
    nltk.data.find("sentiment/vader_lexicon.zip")
except LookupError:
    nltk.download("vader_lexicon")

analyzer = SentimentIntensityAnalyzer()

def analyze_sentiment(text: str) -> dict:
    if not text or not isinstance(text, str):
        raise ValueError("Input text must be a non-empty string")

    scores = analyzer.polarity_scores(text)
    compound = scores["compound"]

    if compound >= 0.05:
        label = "POSITIVE"
    elif compound <= -0.05:
        label = "NEGATIVE"
    else:
        label = "NEUTRAL"

    return {
        "text": text,
        "sentiment_label": label,
        "sentiment_score": compound
    }

def lambda_handler(event, context):
    for record in event.get("Records", []):
        try:
            payload = base64.b64decode(record["body"]).decode("utf-8")
            message = json.loads(payload)

            text = message.get("text")
            if not text:
                logger.warning("Message missing 'text' field: %s", message)
                continue

            result = analyze_sentiment(text)
            logger.info("Sentiment analysis result: %s", json.dumps(result))

        except json.JSONDecodeError:
            logger.error("Invalid JSON format in message")
        except ValueError as ve:
            logger.error("Validation error: %s", ve)
        except Exception as e:
            logger.error("Unexpected error: %s", e)
