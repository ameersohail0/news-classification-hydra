import pandas as pd
from bs4 import BeautifulSoup
import requests

import re
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

import nltk
nltk.download('stopwords')
nltk.download('punkt')
import logging


def web_scrapping(url):
    logging.log(msg=url, level=20)
    url = str(url).replace("'", "").replace('"', '')
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")
    res_h3 = soup.findAll("h3")
    res_h3 = [BeautifulSoup(i.text).findAll("p") for i in res_h3]
    res_h3 = [str(i).encode("ascii", "ignore").decode()
                .replace('<p>', '')
                .replace('</p>', '')
                .replace('[', '')
                .replace(']', '')
                .replace('"', '') for i in res_h3]
    # res_h3 = [process_text(str(i)) for i in res_h3]
    # res_h3 = [i for i in res_h3 if len(str(i)) > 20]
    # for i in res_h3:
    #     if len(str(i)) < 50:
    #         res_h3.remove(i)

    res_h2 = soup.findAll("h3")
    res_h2 = [BeautifulSoup(i.text).findAll("p") for i in res_h2]
    res_h2 = [str(i).encode("ascii", "ignore").decode()
                  .replace('<p>', '')
                  .replace('</p>', '')
                  .replace('[', '')
                  .replace(']', '')
                  .replace('"', '') for i in res_h2]

    # res_h2 = [process_text(str(i)) for i in res_h2]
    # res_h2 = [i for i in res_h2 if len(str(i)) > 20]
    # for i in res_h3:
    #     if len(str(i)) < 50:
    #         res_h3.remove(i)


    res_p = soup.findAll("p")
    res_p = [BeautifulSoup(i.text).findAll("p") for i in res_p]
    res_p = [str(i).encode("ascii", "ignore").decode()
                  .replace('<p>', '')
                  .replace('</p>', '')
                  .replace('[', '')
                  .replace(']', '')
                  .replace('"', '') for i in res_p]
    # res_p = [process_text(str(i)) for i in res_p]
    # res_p = [i for i in res_p if len(str(i)) > 20]
    # for i in res_p:
    #     if len(str(i)) < 50:
    #         res_p.remove(i)

    final_res = res_h3 + res_p + res_h2
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
    # filtered_sentence = []
    # for w in word_tokens:
    #     if w not in stop_words:
    #         filtered_sentence.append(w)

    text = " ".join(filtered_sentence)
    return text

# print(web_scrapping("https://economictimes.indiatimes.com/industry/services/education/the-money-one-needs-to-shell-out-to-become-a-doctor-in-india/articleshow/87389789.cms"))
# print(web_scrapping("https://www.ndtv.com/india-news/mamata-banerjee-in-goa-modiji-more-powerful-because-of-congress-says-mamata-banerjee-from-goa-2593334"))
# print(web_scrapping("https://www.deccanchronicle.com/"))
