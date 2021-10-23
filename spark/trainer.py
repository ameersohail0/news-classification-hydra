# Import training libraries
import pandas as pd
import pickle

import nltk
nltk.download('stopwords')
nltk.download('punkt')

from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
from nltk.tokenize import word_tokenize
from sklearn import preprocessing

import re
import warnings
warnings.filterwarnings("ignore")

def process_text(text):
    pattern = r'[0-9]'
    pattern2 = r'([\.0-9]+)$'
    text = str(text)
    text = re.sub(pattern, '', text)
    text = re.sub(pattern2, '', text)
    text = str(text)
    text = text.lower().replace('\n', ' ').replace('\r', '').strip()
    text = re.sub(' +', ' ', text)
    text = re.sub(r'[^\w\s]', '', text)

    stop_words = set(stopwords.words('english'))
    word_tokens = word_tokenize(text)
    filtered_sentence = [w for w in word_tokens if not w in stop_words]
    filtered_sentence = []
    for w in word_tokens:
        if w not in stop_words:
            filtered_sentence.append(w)

    text = " ".join(filtered_sentence)
    return text