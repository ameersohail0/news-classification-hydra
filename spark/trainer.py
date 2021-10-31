# Import training libraries
import pandas as pd
import pickle

import nltk
nltk.download('stopwords')
nltk.download('punkt')

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
<<<<<<< HEAD
=======
import pandas as pd
>>>>>>> b7d7fd1a6ce26a047c650dd13971dae114b39dd7

import re
import warnings

warnings.filterwarnings("ignore")

category_list = ['POLITICS', "WELLNESS", 'ENTERTAINMENT',
             "STYLE & BEAUTY", "TRAVEL", "PARENTING",
             "FOOD & DRINK", "QUEER VOICES", "HEALTHY LIVING",
             "BUSINESS", "COMEDY", "SPORTS", "HOME & LIVING",
             "BLACK VOICES", "THE WORLDPOST", "WEDDINGS", "PARENTS",
             "DIVORCE", "WOMEN", "IMPACT", "CRIME",
             "MEDIA", "WEIRD NEWS", "WORLD NEWS", "TECH",
             "GREEN", "TASTE", "RELIGION", "SCIENCE",
             "MONEY", "STYLE", "ARTS & CULTURE", "ENVIRONMENT",
             "WORLDPOST", "FIFTY", "GOOD NEWS", "LATINO VOICES",
             "CULTURE & ARTS", "COLLEGE", "EDUCATION", "ARTS"]

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
    # filtered_sentence = []
    # for w in word_tokens:
    #     if w not in stop_words:
    #         filtered_sentence.append(w)

    text = " ".join(filtered_sentence)
    return text