# A script for running the LDA and NMF models on the ETD keyword+abstract data
# Sample code for creating models: https://medium.com/mlreview/topic-modeling-with-scikit-learn-e80d33668730

import logging
import departments
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.decomposition import NMF, LatentDirichletAllocation
from sklearn.feature_extraction import text
from keystracts import KeystractExtractor


etd_stopwords = ['dissertation', 'problem', 'approach', 'method', 'research', 'thesis', 'problems',
                 'report', 'project', 'results', 'using', 'use', 'described', 'designed',
                 'chapter', 'chapters', 'study', 'analysis', 'omitted', 'models', 'proposed', 'work',
                 'ha', 'wa']
stop_words = text.ENGLISH_STOP_WORDS.union(etd_stopwords)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logging.info('loading the documents...')
documents = KeystractExtractor.load_keystracts()


class TopicHandler(object):

    WORDS_PER_TOPIC = 10

    def __init__(self, model,
                 feature_names,
                 doc_titles,
                 tf,
                 department=None,
                 doc_names=None):
        self.tf = tf
        self.model = model
        self.doc_titles = doc_titles
        self.feature_names = feature_names
        self.department = department
        self.doc_names = doc_names

    def display_topics(self):
        if self.department:
            print(self.department)
        for topic_num, topic in enumerate(self.model.components_):
            print("Topic {}: ".format(str(topic_num + 1)), end='')
            print(" ".join([self.feature_names[i]
                            for i in topic.argsort()[:-self.WORDS_PER_TOPIC - 1:-1]]))

    def get_topics(self, words_per):
        """returns a dictionary of topic number IDS paired with the topic words"""
        topics = {}
        try:
            for topic_num, topic in enumerate(self.model.components_):
                topics[topic_num] = " ".join([self.feature_names[i]
                                              for i in topic.argsort()[:-words_per - 1:-1]])
            return topics
        except IndexError:
            return None

    def document_topic_data(self):
        """used to associate topics with documents they most describe"""
        doc_topic = self.model.transform(self.tf)
        doc_titles = KeystractExtractor.get_doc_titles(doc_names=self.doc_names)
        data_dict = {}
        np.savetxt("foo2.csv", doc_topic, delimiter=",")
        for n in range(doc_topic.shape[0]):
            topic_most_pr = doc_topic[n].argmax()
            if topic_most_pr not in data_dict:
                data_dict[topic_most_pr] = [doc_titles[n]]
            else:
                data_dict[topic_most_pr].append(doc_titles[n])
        return data_dict

    def create_department_topic_matrix(self):
        """populate a dictionary of departments with topics (and weights) that best describe them"""
        doc_topic = self.model.transform(self.tf)  # document-topic matrix
        depts = {}
        doc_titles = KeystractExtractor.get_doc_titles()
        dept_names = departments.get_departments()
        # associate documents with departments
        for i, row in enumerate(doc_topic):
            row = list(row)
            max_tup = (row.index(max(row)), max(row))
            for dept in dept_names:
                if doc_titles[i] in dept_names[dept]:
                    if dept not in depts:
                        depts[dept] = [max_tup]
                    else:
                        depts[dept].append(max_tup)
        for d in depts:
            topics = list(set([n for n, _ in depts[d]]))
            new_topics = [(t, sum(n for i, n in depts[d] if i == t)) for t in topics]
            new_val = [0]*NUM_TOPICS
            for i, _ in enumerate(new_val):
                for j in new_topics:
                    if j[0] == i:
                        new_val[i] = j[1]

            new_val.insert(0, d)
            depts[d] = new_val
        for val in list(depts.values()):
            # for now, prints to console. should export as xlsx file.
            print('\t'.join([str(v) for v in val]))

    def save_html(self):
        """saves an explorable web page of document-topic relations"""
        topics = self.get_topics(self.WORDS_PER_TOPIC)
        html_str = "<html><body>"
        if topics:
            doc_data = self.document_topic_data()
            for topic in sorted(self.document_topic_data().keys()):
                html_str += "Topic {}: ".format(str(topic)) + topics[topic] + "<br>"
                print(topics[topic] + "\t" + str(len(doc_data[topic])))
                html_str += ', '.join(
                    ['<a href="http://surface.syr.edu/{}">{}</a>'.format('_'.join(t.split('.')[0].split("_")[:-1]) +
                                                                         '/' + t.split('.')[0].split("_")[-1],
                                                                         t.split('.')[0])
                        for t in doc_data[topic]]) + "<br><br>"
            html_str += "</body></html>"
            file_name = 'document_groupings.html'
            if self.department:
                file_name = "./resources/departments_html/{}2.html".format(self.department)
            with open(file_name, 'w', encoding='utf-8') as html_file:
                html_file.write(html_str)


NUM_FEATURES = 1000
NUM_TOPICS = 50
WORDS_PER_TOPIC = 8


logging.info('Creating vectorizers...')
# Word vectorization for NMF
tfidf_vectorizer = TfidfVectorizer(max_df=0.95,
                                   min_df=3,
                                   max_features=NUM_FEATURES,
                                   stop_words=stop_words)
tfidf = tfidf_vectorizer.fit_transform(documents)
tfidf_feature_names = tfidf_vectorizer.get_feature_names()

# Word vectorization for LDA
count_vectorizer = CountVectorizer(max_df=0.95,
                                   min_df=3,
                                   max_features=NUM_FEATURES,
                                   # ngram_range=(1, 2),
                                   stop_words=stop_words)
raw_count = count_vectorizer.fit_transform(documents)
raw_count_feature_names = count_vectorizer.get_feature_names()


logging.info('Creating NMF model...')
# Create the NMF model
nmf = NMF(n_components=NUM_TOPICS,
          random_state=44,
          alpha=.1,
          l1_ratio=.5,
          init='nndsvd').fit(tfidf)

logging.info('Creating LDA model...')
# Create the LDA model
lda = LatentDirichletAllocation(
    n_components=NUM_TOPICS,
    max_iter=10,
    learning_method='online',
    learning_offset=50.,
    random_state=44
    ).fit(raw_count)


def display_topics(model, feature_names, words_per):
    for topic_num, topic in enumerate(model.components_):
        print("Topic {}: ".format(str(topic_num + 1)), end='')
        print(" ".join([feature_names[i]
                        for i in topic.argsort()[:-words_per - 1:-1]]))


def write_topics(models, features, words_per):
    topic_data = ''
    for k, model in enumerate(models):
        topic_data += 'Model {}\n'.format(str(k))
        for topic_num, topic in enumerate(model.components_):
            topic_data += "Topic {}: ".format(str(topic_num + 1)) + \
                          " ".join([features[k][i]
                                    for i in topic.argsort()[:-words_per-1:-1]]) + '\n'
    with open('./resources/topics.txt', 'w') as topics_file:
        topics_file.write(topic_data)


def main():
    print('NMF Topics: ')
    display_topics(nmf, tfidf_feature_names, WORDS_PER_TOPIC)
    print('\nLDA Topics: ')
    display_topics(lda, raw_count_feature_names, WORDS_PER_TOPIC)
    write_topics([nmf, lda], [tfidf_feature_names, raw_count_feature_names], WORDS_PER_TOPIC)

if __name__ == "__main__":
    main()
    th = TopicHandler(model=lda,
                      feature_names=raw_count_feature_names,
                      tf=raw_count,
                      doc_titles=KeystractExtractor.get_doc_titles())
    th.create_department_topic_matrix()
    th.save_html()
    # th.save_html()
    # topics_by_department()
    #  for item in doc_data:
    #    print(str(item) + " " + str(len(doc_data[item])))
