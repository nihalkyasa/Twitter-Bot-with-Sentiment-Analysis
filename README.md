# Twitter Bot with Sentiment Analysis

In this project, I created a Twitter bot to automatically post responses from a Google Form. From there, I worked to integrate a sentiment analysis model that can filter out negative messages. I am going to walk through my process, and some of the pros and cons of different machine learning models I decided to test.

## The Bot

Overall, the bot itself was a pretty straightforward process. I only ran into hurdles accessing and using Google's and Twitter's APIs. Within Google's API, I had the option of working with the Forms API or the Sheets API. Since the Forms API was more novel than the other and didn't have as much functionality, I worked with the Sheets API and converted my Google Form responses into a Google Sheet. 

There are two main ways to work with the Sheets API: through Google AppScript (similar to JavaScript) or Python. I worked with both but found more long-term success and comfort with Python, but to each their own!

## The Sentiment Analysis

This portion of the project took up the bulk of my time, as it wasn't as straightforward and laid out. I wanted to make a sentiment analysis model that was tailored to the vocabulary of the Twitter account I was working with. For some context, the Twitter account is an "anonymous confessions" type of page that centers around a competitive circuit of Indian dance styles. Due to the traditional nature of Indian dance, there are a lot of words that aren't seen in normally trained models, and I wanted to fine-tune a model to work with these specific tweets. I scraped 2,000+ of the account's most recent tweets and deleted entries that didn't make sense.


