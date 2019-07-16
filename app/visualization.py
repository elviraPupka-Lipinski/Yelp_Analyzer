import matplotlib.pyplot as plt
from wordcloud import WordCloud

# pie chart which shows the distribution of topics
def pie_chart(prediction, top_words, business_id):
    sizes = []
    labels = []
    for i in range(0, len(top_words)):
        # determine sizes
        size_one_Topic = sum(prediction[:, i])
        sizes.append(size_one_Topic)
        label_one_Topic = 'Topic ' + str(i) + ': ' + str(top_words[i][0])
        labels.append(label_one_Topic)

    plt.subplots()
    plt.pie(sizes, autopct='%1.1f%%', startangle=90, counterclock=False)
    plt.legend(labels, loc="best")
    # Equal aspect ratio ensures that the pie is a circle
    plt.axis('equal')
    plt.title("Distribution of topics for business ID :" + business_id)
    plt.tight_layout()
    plt.savefig("pie_chart_"+str(business_id)+".png")
    plt.show()


# visualizes the top words in the reviews of each topic as a word cloud,
# regarding there occurrence in the reviews of the specific business id .
def word_cloud(model, n_top_words, vectorizer, specified_business_id):
    feature_names = vectorizer.get_feature_names()
    for topic_idx, topic in enumerate(model.components_):
        weighted = {}
        pos = topic.argsort()[:-n_top_words - 1:-1]
        for i in pos:
            weighted[feature_names[i]] = topic[i]
        # Creates and generates a word cloud
        wordcloud = WordCloud().generate_from_frequencies(weighted)
        plt.subplots()
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis("off")
        plt.title("Top words of Topic " + str(topic_idx) + " for business ID: " + str(specified_business_id))
        plt.tight_layout()
        plt.savefig("wordcloud_"+str(topic_idx)+"_"+str(specified_business_id)+".png")
        plt.show()


# calculates and plots the avg star rating
def average_star_rating(predictiton, stars, specified_business_id):
    ratings={}
    end_rating = {}
    for i in range(0, len(predictiton)):
        best_topic = predictiton[i].argsort()[-1]
        if(not best_topic in ratings):
            ratings[best_topic]=[]
        ratings[best_topic].append(float(stars[i]))

    for key in ratings.keys():
        print("Topic "+ str(key)+": ")
        calculation = (sum(ratings[key])/len(ratings[key]))
        end_rating.update({key: calculation})
    # sorting the Topics, so that Topic 0 is the first one
    sorted_rating = [(k, end_rating[k]) for k in sorted(end_rating)]
    topics = ([ 'Topic '+ str(x[0]) for x in sorted_rating])
    calculated_avg_stars = [x[1] for x in sorted_rating]
    plt.subplots()
    plt.bar(topics,calculated_avg_stars)
    plt.ylabel('AVG Stars')
    plt.title('Average Stars for business ID: ' + str(specified_business_id))
    plt.show()