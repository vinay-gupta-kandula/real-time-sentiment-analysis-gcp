import unittest
import sys
import os

# Allow import from sentiment_analyzer directory
sys.path.insert(
    0,
    os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "sentiment_analyzer"))
)

from main import analyze_sentiment


class TestSentimentAnalyzer(unittest.TestCase):

    def test_positive_sentiment(self):
        result = analyze_sentiment("I absolutely love this product, it's fantastic!")
        self.assertEqual(result["sentiment_label"], "POSITIVE")
        self.assertGreater(result["sentiment_score"], 0.05)

    def test_negative_sentiment(self):
        result = analyze_sentiment("This was a terrible experience, very disappointing.")
        self.assertEqual(result["sentiment_label"], "NEGATIVE")
        self.assertLess(result["sentiment_score"], -0.05)

    def test_neutral_sentiment(self):
        result = analyze_sentiment("The item arrived on time, as described.")
        self.assertEqual(result["sentiment_label"], "NEUTRAL")

    def test_empty_string(self):
        with self.assertRaises(ValueError):
            analyze_sentiment("")

    def test_non_string_input(self):
        with self.assertRaises(ValueError):
            analyze_sentiment(123)


if __name__ == "__main__":
    unittest.main()
