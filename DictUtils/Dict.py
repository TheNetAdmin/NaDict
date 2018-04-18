"""Maintain dictionary"""

import json
import codecs
import os
from urllib.parse import urlencode
from urllib.request import urlopen
import logging


class Dictionary(object):
    __api_base_url = 'http://fanyi.youdao.com/openapi.do?' + \
                     'keyfrom=POTDictionary&key=1430652075&type=data&doctype=json&version=1.1&'

    def __init__(self, dict_filename: str()):
        self.dict_file = None
        self.dict_filename = os.path.abspath(dict_filename)
        self.dict_is_dirty = False
        self.logger = logging.getLogger('UTILS.Dict')
        self.__open_dict()
        self.total_words = 0
        self.not_known_words = 0

    def __del__(self):
        if self.dict_is_dirty is True:
            self.__save_dict()
        percent = self.not_known_words / self.total_words * 100
        self.logger.info('Not known words: ' + str(percent) + '%')

    def __open_dict(self):
        dict_content = str()
        with codecs.open(self.dict_filename, 'r', 'utf-8') as dict:
            dict_content = dict.read()
        self.dict_file = json.loads(dict_content)

    def __save_dict(self):
        with codecs.open(self.dict_filename, 'w', 'utf-8') as dict:
            dict_content = json.dumps(self.dict_file, ensure_ascii=False)
            dict.write(dict_content)

    def __fetch(self, word: str()):
        self.logger.info("Translating word [" + word + "] online.")
        query = {'q': word}
        url = self.__api_base_url + urlencode(query)
        response = urlopen(url, timeout=3)
        result = response.read().decode('utf-8')
        return json.loads(result)

    def look_up(self, word: str()):
        self.total_words += 1
        result = self.dict_file.get(word)
        if result is None:
            self.not_known_words += 1
            # translate online, add to dict, then set result
            result = self.__fetch(word)
            self.dict_file[word] = result
            # set dirty
            if self.dict_is_dirty is False:
                self.dict_is_dirty = True
        return result
