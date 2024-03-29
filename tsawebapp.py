# -*- coding: utf-8 -*-
"""Web_App.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/11ZOmfCqtUQRuRT6sXblYXrlPooAj_OQt
"""
print("Importing modules...")
import streamlit as st
import emoji
import pandas as pd
import re,string
import pickle
import nltk
from nltk.stem import WordNetLemmatizer
import sqlite3 
print("Importing completed...")
wnl = WordNetLemmatizer()
nltk.download('wordnet')
nltk.download('omw-1.4')

conn = sqlite3.connect('data.db')
c = conn.cursor()

def create_table():
	c.execute('CREATE TABLE IF NOT EXISTS tweetTable(tweet TEXT,sentiment TEXT)')


def add_data(tweet,sentiment):
	c.execute('INSERT INTO tweetTable(tweet,sentiment) VALUES (?,?)',(tweet,sentiment))
	conn.commit()
    
def view_all_tweets():
	c.execute('SELECT * FROM tweetTable')
	data = c.fetchall()
	return data
    

def data_preprocesing(tweet):
  tokens = []

  for token in tweet.split():
    tokens.append(wnl.lemmatize(token,pos="v"))
  tweet =  " ".join(tokens)
  
    
  return "".join(tweet)
  


def replace_contractions(t):
  '''
  This function replaces english lanuage contractions like "shouldn't" with "should not"
  '''
  cont = {"aren't" : 'are not', "can't" : 'cannot', "couln't": 'could not', "didn't": 'did not', "doesn't" : 'does not',
  "hadn't": 'had not', "haven't": 'have not', "he's" : 'he is', "she's" : 'she is', "he'll" : "he will", 
  "she'll" : 'she will',"he'd": "he would", "she'd":"she would", "here's" : "here is", 
   "i'm" : 'i am', "i've"	: "i have", "i'll" : "i will", "i'd" : "i would", "isn't": "is not", 
   "it's" : "it is", "it'll": "it will", "mustn't" : "must not", "shouldn't" : "should not", "that's" : "that is", 
   "there's" : "there is", "they're" : "they are", "they've" : "they have", "they'll" : "they will",
   "they'd" : "they would", "wasn't" : "was not", "we're": "we are", "we've":"we have", "we'll": "we will", 
   "we'd" : "we would", "weren't" : "were not", "what's" : "what is", "where's" : "where is", "who's": "who is",
   "who'll" :"who will", "won't":"will not", "wouldn't" : "would not", "you're": "you are", "you've":"you have",
   "you'll" : "you will", "you'd" : "you would", "mayn't" : "may not"}
  words = t.split()
  reformed = []
  for w in words:
    if w in cont:
      reformed.append(cont[w])
    else:
      reformed.append(w)
  t = " ".join(reformed)
  return t  

def remove_single_letter_words(t):
  '''
  This function removes words that are single characters
  '''
  words = t.split()
  reformed = []
  for w in words:
    if len(w) > 1:
      reformed.append(w)
  t = " ".join(reformed)
  return t  


def de_emoji(tweet):
  tweet = emoji.demojize(tweet)
  tweet = tweet.replace(":"," ")
  return ' '.join(tweet.split())


def dataclean(t):
  '''
  This function cleans the tweets.
  '''
  t = t.lower() # convert to lowercase
  t = replace_contractions(t) # replace short forms used in english  with their actual words
  t = de_emoji(t) # replace unicode emojis with their feeling associated
  t = re.sub('\\\\u[0-9A-Fa-f]{4}','', t) # remove NON- ASCII characters
  t = re.sub("[0-9]", "", t) # remove numbers # re.sub("\d+", "", t)
  t = re.sub('#', '', t) # remove '#'
  t = re.sub('@[A-Za-z0–9]+', '', t) # remove '@'
  t = re.sub('@[^\s]+', '', t) # remove usernames
  t = re.sub('RT[\s]+', '', t) # remove retweet 'RT'
  t = re.sub('((www\.[^\s]+)|(https?://[^\s]+))', '', t) # remove links (URLs/ links)
  t = re.sub('[!"$%&\'()*+,-./:@;<=>?[\\]^_`{|}~]', '', t) # remove punctuations
  t = t.replace('\\\\', '')
  t = t.replace('\\', '')
  t = remove_single_letter_words(t) # removes single letter words
  t = data_preprocesing(t)
  
  return t
  
  
new_vectorizer = pickle.load(open("./new_nlpcountvectorizer.pkl","rb"))
new_model = pickle.load(open("./new_nbcountmodel.pkl","rb"))
  
def new_predict_sentiment(tweet):
  tweet = data_preprocesing(tweet)
  tweet = dataclean(tweet)
  tweet = new_vectorizer.transform([tweet])
  y_pred = new_model.predict(tweet)
  return y_pred[0]


print("Streamlit is on...")
st.title('Tweeter Sentiment Analysis')
st.sidebar.header('Project by :')
st.sidebar.text('1. Yash Dattatraya Pawar')
st.sidebar.text('2. Piyush Vijay Misar')
if st.sidebar.button("View Tweets"):
    Tweet_result = view_all_tweets()
    clean_db = pd.DataFrame(Tweet_result,columns=["Tweet","Sentiment"])
    st.sidebar.dataframe(clean_db)
    

tweet = st.text_input('Enter the Tweet',max_chars=280)
create_table()

if st.button("Enter"):
    sentiment = new_predict_sentiment(tweet)
    if sentiment == 1:
      st.write('Tweet is Positive 😃')
      sentiment = "Positive"
    elif sentiment == 0:
      st.write('Tweet is Negative 😥')
      sentiment = "Negative"
    add_data(tweet,sentiment)
