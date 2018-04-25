from os import listdir
import json
from nltk.stem import WordNetLemmatizer
from nltk.stem.snowball import SnowballStemmer


class KeystractExtractor:

    ENCODING = 'utf-8'

    def __init__(self,
                 doc_dir='./resources/keystracts',
                 filename='keystracts.json'
                 ):
        self.doc_dir = doc_dir
        self.filename = filename
        self._lemmatizer = WordNetLemmatizer()
        self._stemmer = NullStemmer()

    def get_documents_from_files(self, doc_names=None):
        file_contents = []
        for fn in listdir(self.doc_dir):
            if not doc_names or fn in doc_names:
                with open(self.doc_dir + '/' + fn, 'r', encoding=self.ENCODING) as text_file:
                    # apply lemmatization at this stage
                    file_contents.append(' '.join(
                        [self._stemmer.stem(self._lemmatizer.lemmatize(token))
                         for token in text_file.read().split(' ')]))
        return file_contents

    def create_json_file(self, filename="keystracts.json"):
        with open("./resources/{}".format(filename), 'w', encoding=self.ENCODING) as json_file:
            json.dump(self.get_documents_from_files(), json_file)

    @staticmethod
    def load_keystracts(file_path='./resources/keystracts.json'):
        with open(file_path, 'r', encoding='utf-8') as json_file:
            return json.load(json_file)

    @staticmethod
    def get_doc_titles(doc_dir='./resources/keystracts', doc_names=None):
        if doc_names:
            return [filename for filename in listdir(doc_dir) if filename in doc_names]
        return [filename for filename in listdir(doc_dir)]


class NullLemmatizer:

    def __init__(self):
        """dummy class for de-lemmatization"""
        pass

    @staticmethod
    def lemmatize(token):
        return token


class NullStemmer:

    def __init__(self):
        """dummy class for de-stemming"""
        pass

    @staticmethod
    def stem(token):
        return token


if __name__ == "__main__":
    # run JSON dataset creation with default parameters
    ke = KeystractExtractor()
    ke.create_json_file()
    # docs = ke.get_doc_titles()
    # for d in docs:
    #     print(d.split('.')[0])
    # ke.create_json_file()
