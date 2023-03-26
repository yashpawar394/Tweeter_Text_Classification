# -*- coding: utf-8 -*-
"""sentiment_analysis_autokeras.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/17QOVfzAXBaJ0r3PFHElsOGPdIbxn4qBm
"""

from google.colab import drive
drive.mount('/content/drive')

!pip install autokeras

!pip install emoji

import tensorflow as tf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import re,os

from sklearn.datasets import load_files
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report,confusion_matrix

import autokeras as ak
import emoji

!unzip "/content/drive/MyDrive/datasets/tweeter_tweet_datasets.csv"

col_names = ["target","ids","date","flag","user","content"]

df = pd.read_csv('/content/drive/MyDrive/datasets/tweeter_tweet_datasets.csv',delimiter=',',names=col_names ,encoding = "latin-1")

df.info()

df = df[['target','content']]

df.info()

"""Target column Notations

4 = Possitive

0 = Negative
"""

df['target'] = df['target'].replace([0, 4],['Negative','Positive'])

df['target'].value_counts()

sns.countplot(x='target',hue='target',data=df)

df.target = df.target.replace({'Positive': 1, 'Negative': 0})

def de_emoji(tweet):
  tweet = emoji.demojize(tweet)
  tweet = tweet.replace(":"," ")
  return ' '.join(tweet.split())

text = "He is 😳,game is on 🔥 🔥"
de_emoji(text)

def data_preprocesing(t):
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
  
  # convert the text to lower case
  t = t.lower()
    
  return "".join(t)

data_preprocesing('Hey @Yash how are you,www.quora.com')

df['content'] = df['content'].apply(data_preprocesing)

df['content'] = df['content'].apply(de_emoji)

df['content'].values

x = df['content']
y = df['target']

x_train,x_test,y_train,y_test = train_test_split(x,y, test_size=0.1, random_state=7)

x_train.shape, x_test.shape, y_train.shape, y_test.shape

x_train = np.array(x_train)
y_train = np.array(y_train)
x_test = np.array(x_test)
y_test = np.array(y_test)
print(type(x_test))
print(x_train.shape)  # (25000,)
print(y_train.shape)  # (25000, 1)
print(x_train[0][:50])  # this film was just brilliant casting
print(x_test.shape)  # (25000,)
print(y_test.shape)  # (25000, 1)

# Initialize the text classifier.
clf = ak.TextClassifier(
    overwrite=True, max_trials=1) 

 # It only tries 1 model as a quick demo.
# Feed the text classifier with training data.
clf.fit(x_train, y_train, epochs=5)

# Predict with the best model.
predicted_y = clf.predict(x_test)

# Evaluate the best model with testing data.
print(clf.evaluate(x_test, y_test))

from sklearn.metrics import classification_report
print(x_test[0])
y_pred = clf.predict(x_test)
# print(classification_report(y_test, y_hat))

model2 = clf.export_model()

model2.summary()

from tensorflow.keras.models import load_model

model2.save('/content/drive/MyDrive/Colab Notebooks')

y_pred

res = y_pred.astype(np.int)
res = res.flatten()

res

y_test

print(classification_report(y_test, res))

from mlxtend.plotting import plot_confusion_matrix

conf_matrix = confusion_matrix(y_true=y_test, y_pred=res)

fig, ax = plot_confusion_matrix(conf_mat = conf_matrix, figsize=(7.5, 12), cmap=plt.cm.Blues)
plt.xlabel('Predictions', fontsize=18)
plt.ylabel('Actual', fontsize=18)
plt.title('Confusion Matrix', fontsize=18)
plt.show()