import pickle

import pandas as pd
import nltk

nltk.download('stopwords')
nltk.download('punkt')
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfTransformer, CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn import svm
from nltk.tokenize import word_tokenize
from sklearn.calibration import CalibratedClassifierCV

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


# training_data = pd.read_csv('train_data.csv', encoding='utf-8', sep='\t')
training_data = pd.read_json('/app/data/news_new.json', encoding='utf-8')
training_data = training_data.dropna()
training_data['short_description'] = training_data['short_description'].apply(process_text)

count_vect = CountVectorizer()
X_train_counts = count_vect.fit_transform(training_data.data)
tfidf_transformer = TfidfTransformer()
X_train_tfidf = tfidf_transformer.fit_transform(X_train_counts)

X_train, X_test, y_train, y_test = train_test_split(X_train_tfidf, training_data.flag,
                                                    test_size=0.25, random_state=9)

svm = svm.LinearSVC()

model = CalibratedClassifierCV(svm)
model.fit(X_train_tfidf, training_data.flag)

pickle.dump(count_vect.vocabulary_, open("/app/models/count_vector.pkl", "wb"))
pickle.dump(tfidf_transformer, open("/app/models/tfidf.pkl", "wb"))
pickle.dump(model, open("/app/models/news_classifier.pkl", "wb"))

predictions = model.predict(X_test)
y_prob = model.predict_proba(X_test)

probability = []

for prediction, proba in zip(predictions, y_prob):
    probability.append(proba[prediction])
#
# for prediction, prob in zip(predictions, probability):
#     print(category_list[prediction] + " - " + str(prob*100))
