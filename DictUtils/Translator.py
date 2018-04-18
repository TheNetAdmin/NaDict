"""Translate the word lists, output as json file"""

import json
import os
import codecs
from urllib.parse import urlencode
from urllib.request import urlopen
import logging


class WordRecord(object):
    def __init__(self):
        self.list_no = 0
        self.data = None

    def loads(self, list_no: int, data: dict()):
        self.list_no = list_no
        self.data = data

    def dumps(self):
        ret = {'list_no': self.list_no, 'data': self.data}
        return ret


class Translator(object):
    """Translate using API, output as json file"""
    # Register your api and fill this url
    __api_base_url = 'http://fanyi.youdao.com/openapi.do?' + \
                     ''

    def __init__(self):
        self.src_filename = ''
        self.out_filename = ''
        self.src_file = None
        self.out_file = None
        self.word_lists = None
        self.translated_word_lists = list()
        self.logger = logging.getLogger('UTILS.Translator')

    def __process_filename(self, src_filename: str()):
        src_filename = os.path.abspath(src_filename)
        dir_name = os.path.dirname(src_filename)
        base_name = os.path.basename(src_filename)
        base_name = os.path.splitext(base_name)[0]
        self.src_filename = src_filename
        self.out_filename = os.path.join(
            dir_name, base_name + '-translated.json')

    def __open_src_file(self):
        with codecs.open(self.src_filename, 'r', 'utf-8') as src:
            self.src_file = src.read()

    def __parse_src_file(self):
        self.word_lists = json.loads(self.src_file)

    def __translate_all(self, dictionary):
        for single_list in self.word_lists:
            list_no = single_list['list_no']
            for word in single_list['words']:
                translation = dictionary.look_up(word)
                record = WordRecord()
                record.loads(list_no, translation)
                self.translated_word_lists.append(record.dumps())

    def __write_out_file(self):
        with codecs.open(self.out_filename, 'w', 'utf-8') as out:
            out.write(json.dumps(self.translated_word_lists, ensure_ascii=False))
        self.logger.info("Words' translation output to " + self.out_filename)

    def translate(self, src_filename: str(), dictionary):
        self.__process_filename(src_filename)
        self.__open_src_file()
        self.__parse_src_file()
        self.__translate_all(dictionary)
        self.__write_out_file()
        return self.out_filename

    def clean(self):
        os.remove(self.out_filename)