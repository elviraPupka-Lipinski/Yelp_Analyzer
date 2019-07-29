import dataPreprocessing
import vectorizeAndTrain
import visualization
import argparse
import pickle

parser = argparse.ArgumentParser(description='Yelp dataset Analyzer')
parser.add_argument("--businessID", help="ID of the business to be analyzed")
args = parser.parse_args()
if (args.businessID is not None):
    specified_business_id= args.businessID
else:
    specified_business_id = "c0yPNU-BqS65u0vIKP7P0w"


city = "Pittsburgh"
category = "Restaurant"


"""
Business_ids:
006 = {str} 'c0yPNU-BqS65u0vIKP7P0w'
008 = {str} 'hDD6-yk1yuuRIvfdtHsISg'
000 = {str} 'dQj5DLZjeDK3KFysh1SYOQ'
007 = {str} 'qHseX2NHeUUedIgs_VasZA'
003 = {str} 'hzyvL2v97xLzLbLXcdi1uw'
005 = {str} 'X8AGCsJHw-GuTqkzy2J3cg'
002 = {str} 'Mv7N0bU56dhtoDP-m2JOow'
004 = {str} 'uRybQLCYWkC6N19MhaHf_w'
001 = {str} 'sMzNLdhJZGzYirIWt-fMAg'
010 = {str} '7z2x16M7IuG8KPfMsyVrKA'
009 = {str} '3TrY8CpsnvnTTYigx2R4yg'
011 = {str} 'nlVjdQq9FzdQ3bfy-8y80g'
"""

# extracts the business id for a specific city and category
business_ids_one_city = dataPreprocessing.extract_business_ids_from_one_city(city, category, 'app/business.json')

# extracts the raw reviews for the business ids
raw_reviews = dataPreprocessing.extract_texts(business_ids_one_city, category,city)

# preprocessed reviews
list_lemmatized=dataPreprocessing.text_preprocessing(raw_reviews, category,city)


# vectorizes and trains the model
vectorizer, lda =vectorizeAndTrain.vectorize_and_train(list_lemmatized, category, city)


# extracts the raw reviews for a specific business id
request_reviews = dataPreprocessing.request_data_extraction(specified_business_id)


# preprocesses and predicts the raw reviews
predictiton, top_words, stars = vectorizeAndTrain.predict_and_vectorize(request_reviews, lda, vectorizer, category,city)



#visualizations
visualization.pie_chart(predictiton, top_words, specified_business_id)
visualization.word_cloud(lda, 5, vectorizer)
visualization.average_star_rating(predictiton, stars, specified_business_id)