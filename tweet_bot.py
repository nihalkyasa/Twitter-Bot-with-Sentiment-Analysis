from __future__ import print_function

import os

import pickle
from google_auth_oauthlib.flow import Flow, InstalledAppFlow
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
from google.auth.transport.requests import Request
from googleapiclient.errors import HttpError

import twitter_keys as tk
import tweepy

import string
import nltk
import textblob
import vaderSentiment

nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer



def make_service():

    creds = None

    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', scopes)

    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', scopes)
            creds = flow.run_local_server(port=0)

        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        service = build('sheets', 'v4', credentials=creds)
        return service
    except HttpError as err:
        print(err)


client_secret_file = 'credentials.json'
api_name = 'sheets'
api_version = 'v4'
scopes = ['https://www.googleapis.com/auth/spreadsheets']

service = make_service()
spreadsheet_id = '1sYwn60izDCDe5LACjgV7LN2rL4BcMVqHtB-LMzrKu6Q'
sheet_id = '1227961121'


def get_last_response():
    response = service.spreadsheets().values().get(
        spreadsheetId=spreadsheet_id,
        range='Form Responses 1!A2:C'
    ).execute()

    last_row_idx = len(response['values']) - 1
    last_response = response['values'][last_row_idx][1]
    return last_response


stopwords = nltk.corpus.stopwords.words('english')
lemmatizer = WordNetLemmatizer()

def clean(text):
    no_punc = ''.join([word for word in text if word not in string.punctuation])
    lowercase = no_punc.lower()
    tokens = nltk.word_tokenize(lowercase)
    no_stops = [word for word in tokens if word not in stopwords]
    lemmatized = [lemmatizer.lemmatize(word, pos='v') for word in no_stops]
    clean_text = ' '.join([word for word in lemmatized])
    return clean_text


analyzer = SentimentIntensityAnalyzer()

def compound_sentiment(text):
    sentiment = TextBlob(text).sentiment
    sentiment_analysis = analyzer.polarity_scores(text)
    compound_score = sentiment_analysis['compound']
    if compound_score <= -0.20:
        return 'Negative'
    elif compound_score >= 0.05:
        return 'Positive'
    else:
        return 'Neutral'


api_key = tk.api_key
api_key_secret = tk.api_key_secret
access_token = tk.access_token
access_token_secret = tk.access_token_secret
bearer_token = tk.bearer_token


def post_tweet(message):
    client = tweepy.Client(bearer_token=bearer_token,
                           consumer_key=api_key,
                           consumer_secret=api_key_secret,
                           access_token=access_token,
                           access_token_secret=access_token_secret,
                           wait_on_rate_limit=True)

    client.create_tweet(text=message)


def main():
    tweet_content = get_last_response()
    clean_tweet = clean(tweet_content)
    if compound_sentiment(clean_tweet) != 'Negative':
        post_tweet(tweet_content)


if __name__ == '__main__':
    main()
