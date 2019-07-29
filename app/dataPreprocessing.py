import json
import spacy
import pickle
import re
from spacy.lang.en.stop_words import STOP_WORDS
from langdetect import detect
import os.path

# extracting the business_ids with regard to the given category and city. This task is fast, so I decided not to save the output
# Just for training
def extract_business_ids_from_one_city(city, category, path):
    with open(path, 'rb') as f:
        business_ids_one_city = []
        for line in f:
            dictLine = json.loads(line)
            if dictLine['city'] == city:
                if dictLine['categories'] is not None and category in dictLine['categories']:
                    business_ids_one_city.append(dictLine['business_id'])
    return business_ids_one_city



# extracts the review texts with specific business ids and saves the output
# just for training
def extract_texts(business_ids_one_city, category, city):
    path = 'app/rawreviews_' + category + "_" + city + ".pkl"
    raw_reviews = []
    # loading file if already exists
    if path and os.path.isfile(path):
        f = open(path, 'rb')
        raw_reviews = pickle.load(f)
        f.close()
    else:
        with open('app/review.json', "rb", ) as f:
            for line in f:
                dictLine = json.loads(line)
                if dictLine['business_id'] in business_ids_one_city:
                    # done because detection throws an error if a language can not be detected, such as reviews with only numbers
                    try:
                        if (detect(dictLine['text']) == "en"):
                            raw_reviews.append(dictLine['text'])
                    except:
                        pass
        # saving the reviews
        output = open(path, 'wb')
        pickle.dump(raw_reviews, output)
        output.close()
    return raw_reviews


# preprocessing the raw reviews.
def text_preprocessing(raw_reviews, category, city,request=False):
    path = 'app/lemmatized_' + category + "_" + city + ".pkl"
    length = len(raw_reviews)
    list_lemmatized = []
    if path and os.path.isfile(path) and not request:
        f = open(path, 'rb')
        bool = True
        while bool:
            try:
                help = pickle.load(f)
                list_lemmatized.extend(help)
            except EOFError:
                bool = False
        f.close()
    else:
        for i in range(0, length):
            nlp = spacy.load('en_core_web_sm')

            spacy_doc = (raw_reviews[i])

            # lower
            lower = "".join([tok.lower() for tok in spacy_doc])
            # Punctuation
            no_punctuation = " ".join([tok.text for tok in nlp(lower) if re.match('\w+', tok.text)])

            # tokenization
            test = ([tok.text for tok in nlp(no_punctuation)])

            # removing number
            no_numbers = ([tok for tok in test if not re.match('\d+', tok)])

            # adding a few stop words
            nlp.Defaults.stop_words |= {'great', 'best', 'good', 'better', 'best', 'greater'}
            # removing stop words
            stop_words = " ".join([tok for tok in no_numbers if tok not in STOP_WORDS])

            #lemmatization
            lemmatized = " ".join([tok.lemma_ for tok in nlp(stop_words)])

            list_lemmatized.append(lemmatized)
            if i % 500 == 0 and i != 0 or i == length - 1 and not request:
                output = open(path, 'ab+')
                pickle.dump(list_lemmatized, output)
                output.close()
                list_lemmatized.clear()
        if not request:
            f = open(path, 'rb')
            bool = True
            while bool:
                try:
                    help = pickle.load(f)
                    list_lemmatized.extend(help)
                except EOFError:
                    bool = False
            f.close()
    return list_lemmatized



#extracting the reviews and stars for the requested business
def request_data_extraction(business_id):
    with open("app/review.json", 'rb') as f:
        extracted_data = []
        for line in f:
            dictLine = json.loads(line)
            if dictLine['business_id'] == business_id:
                review = dictLine['text']
                stars = dictLine['stars']
                extracted_data.append((review, stars))
    return extracted_data