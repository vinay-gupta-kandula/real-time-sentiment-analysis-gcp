import unittest
import sys
import os

# Link to the analyzer folder
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'sentiment_analyzer')))
from main import analyze_sentiment

class TestSentiment(unittest.TestCase):
    def test_positive(self):
        res = analyze_sentiment("Great product!")
        self.assertEqual(res['sentiment_label'], 'POSITIVE')

    def test_negative(self):
        res = analyze_sentiment("This is bad.")
        self.assertEqual(res['sentiment_label'], 'NEGATIVE')

    def test_invalid(self):
        with self.assertRaises(ValueError):
            analyze_sentiment("")

if __name__ == '__main__':
    unittest.main()