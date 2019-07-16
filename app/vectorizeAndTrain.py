import pickle
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation
import os.path
import dataPreprocessing

# vectorizing and training the lda model. vectorizer is not saved, due to its fast computation time
def vectorize_and_train(lemmatized_reviews, category, city):
    path = 'app/lda_' + category + "_" + city + ".pkl"

    vectorizer = CountVectorizer(ngram_range=(1, 1), stop_words='english')
    vec = vectorizer.fit_transform(lemmatized_reviews)

    if path and os.path.isfile(path):
        f = open(path, 'rb')
        lda = pickle.load(f)
        f.close()
    else:

        lda = LatentDirichletAllocation(n_components=5, max_iter=50,
                                        learning_method='online',
                                        learning_offset=50.,
                                        random_state=0)
        #training lda
        lda.fit(vec)
        #saving lda
        output = open(path, 'wb')
        pickle.dump(lda, output)
        output.close()

    return vectorizer,lda

# vectorizing the reviews from the requested business and predicting its topics
def predict_and_vectorize(extracted_data, model, vectorizer, category, city):
    reviews = [x[0] for x in extracted_data]
    stars = [x[1] for x in extracted_data]

    # preprocessing of the business' review
    lemmatized = dataPreprocessing.text_preprocessing(reviews,category, city, True)
    vectorized_reviews = vectorizer.transform(lemmatized)
    # prediction
    prediction = model.transform(vectorized_reviews)
    predicted_feature_names = vectorizer.get_feature_names()
    # getting the top 5 words within a topic
    top_words = get_top_words(model, predicted_feature_names, 5)
    return prediction, top_words, stars

# extracting the n top words
def get_top_words(model, feature_names, n_top_words):
    topic_list = []
    components = model.components_
    for topic_idx, topic in enumerate(model.components_):
        topic_list.append([feature_names[i]
                           for i in topic.argsort()[:-n_top_words - 1:-1]])

    return topic_list