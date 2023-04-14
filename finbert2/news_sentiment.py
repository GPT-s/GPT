# news_sentiment.py

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import requests
from bs4 import BeautifulSoup
from transformers import pipeline

def analyze_sentiment(text):
    model_name = "ProsusAI/finbert"
    classifier = pipeline('sentiment-analysis', model=model_name)
    result = classifier(text)[0]
    label = result['label']
    scores = result['score']
    return label, scores

def sentiment_result(text) :
    sentiment_result = analyze_sentiment(text)
    label = sentiment_result[0]
    scores = sentiment_result[1]
    
    print(f"Text: {text}")
    print(f"Sentiment: {label}")
    print(f"Score: {scores}")

  
