
import json
import codecs
from DictUtils.IncProducer import IncProducer
from DictUtils.Dict import Dictionary

class WordMode(object):
    def __init__(self):
        self.dictionary = None

    def start(self, dict_filename: str(), src_filename: str()):
        # with codecs.open(dict_filename, 'r', 'utf-8') as df:
        #     content = df.read()
        #     self.dictionary = json.loads(content)
        self.dictionary = Dictionary(dict_filename)
        inc = IncProducer()
        inc.produce(src_filename, self.dictionary)