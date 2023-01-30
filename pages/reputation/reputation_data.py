from pages.sentiment.sentiment_data import get_sentiment_count
import pandas as pd

sentiment_count = get_sentiment_count()

total = sentiment_count['Count'].sum()
positive = sentiment_count[sentiment_count['Sentiment'].str.lower() == 'positive']['Count']
negative = sentiment_count[sentiment_count['Sentiment'].str.lower() == 'negative']['Count']
neutral = sentiment_count[sentiment_count['Sentiment'].str.lower() == 'neutral']['Count']

def get_NBR():
    return round(((int(positive)-int(negative))/total)*100,2)
    return "{:0.2f}%".format(nbp) 

def get_BFT():
    return round(((int(positive)+int(neutral)-int(negative))/total)*100,2)
    return "{:0.2f}%".format(bft)