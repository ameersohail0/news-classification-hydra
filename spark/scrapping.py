import pandas as pd
from bs4 import BeautifulSoup
import requests
import re

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import nltk

nltk.download('stopwords')
nltk.download('punkt')


def web_scrapping(url):
    r = requests.get(str(url))
    soup = BeautifulSoup(r.text, "html.parser")

    res_p = soup.findAll("p")
    res_p = [BeautifulSoup(i.text, features="lxml").findAll("p") for i in res_p]
    res_p = [str(i).encode("ascii", "ignore").decode()
                 .replace('<p>', '')
                 .replace('</p>', '')
                 .replace('[', '')
                 .replace(']', '')
                 .replace('"', '') for i in res_p]

    res_h4 = soup.findAll("h4")
    res_h4 = [BeautifulSoup(i.text, features="lxml").findAll("p") for i in res_h4]
    res_h4 = [str(i).encode("ascii", "ignore").decode()
                  .replace('<p>', '')
                  .replace('</p>', '')
                  .replace('[', '')
                  .replace(']', '')
                  .replace('"', '') for i in res_h4]

    res_h3 = soup.findAll("h3")
    res_h3 = [BeautifulSoup(i.text, features="lxml").findAll("p") for i in res_h3]
    res_h3 = [str(i).encode("ascii", "ignore").decode()
                  .replace('<p>', '')
                  .replace('</p>', '')
                  .replace('[', '')
                  .replace(']', '')
                  .replace('"', '') for i in res_h3]

    res_h2 = soup.findAll("h2")
    res_h2 = [BeautifulSoup(i.text, features="lxml").findAll("p") for i in res_h2]
    res_h2 = [str(i).encode("ascii", "ignore").decode()
                  .replace('<p>', '')
                  .replace('</p>', '')
                  .replace('[', '')
                  .replace(']', '')
                  .replace('"', '') for i in res_h2]

    res_h1 = soup.findAll("h1")
    res_h1 = [BeautifulSoup(i.text, features="lxml").findAll("p") for i in res_h1]
    res_h1 = [str(i).encode("ascii", "ignore").decode()
                  .replace('<p>', '')
                  .replace('</p>', '')
                  .replace('[', '')
                  .replace(']', '')
                  .replace('"', '') for i in res_h1]

    final_res = res_p + res_h1 + res_h2 + res_h3 + res_h4
    final_res = set(final_res)
    final_res = list(final_res)
    final_res = [i for i in final_res if len(str(i)) > 20]

    original_data = final_res
    final_res = [process_text(str(i)) for i in final_res]

    df = pd.DataFrame(final_res, columns=['data'])

    return df, original_data


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

    text = " ".join(filtered_sentence)
    return text
