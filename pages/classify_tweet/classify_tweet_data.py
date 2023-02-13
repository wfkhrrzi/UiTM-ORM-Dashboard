from env.config import BERTOPIC_HOST,SENTIMENT_HOST
import requests

def sentiment_predict(input_tweet):
    return requests.get(f"{SENTIMENT_HOST}/predict?tweets={input_tweet}").json()

def topic_predict(input_tweet):
    return requests.get(f"{BERTOPIC_HOST}/predict?tweets={input_tweet}").json()
