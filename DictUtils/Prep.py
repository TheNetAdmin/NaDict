"""This module is use to pre-process word list file"""

import json
import codecs
import re
import os
import logging


class ListRecord(object):
    """Used to record one word list, which contains a list of words"""

    def __init__(self):
        self.data = {'list_no': 0, 'words': ''}

    def loads(self, list_no: int, single_list: list(), sort):
        """Load data from one single list(as a whole string)"""
        words = re.split(r'\s', single_list)
        while '' in words:
            words.remove('')
        if sort is True:
            words.sort()
        self.data['list_no'] = list_no
        self.data['words'] = words

    def dumps(self):
        """Dump word list data as json"""
        return json.dumps(self.data)


class Prep(object):
    """Used to pre-process word list file, split into several lists, output as json"""

    def __init__(self):
        self.src_filename = ''
        self.out_filename = ''
        self.src_file = None
        self.out_file = None
        self.lists_parsed = list()
        self.logger = logging.getLogger('UTILS.Prep')

    def __del__(self):
        pass

    def __process_filename(self, src_filename: str()):
        src_filename = os.path.abspath(src_filename)
        dir_name = os.path.dirname(src_filename)
        base_name = os.path.basename(src_filename)
        base_name = os.path.splitext(base_name)[0]
        self.src_filename = src_filename
        self.out_filename = os.path.join(dir_name, base_name + '.json')

    def __open_src_file(self):
        with codecs.open(self.src_filename, 'r', 'utf-8') as src:
            self.src_file = src.read()

    def __parse_src_file(self, basic_list_no: int, sort):
        # Separate into several word lists
        lists = re.split(r'---.*\n', self.src_file)
        while '' in lists:
            lists.remove('')
        # Process each word list
        list_no = basic_list_no
        for single_list in lists:
            record = ListRecord()
            record.loads(list_no, single_list, sort)
            list_no += 1
            self.lists_parsed.append(record.data)

    def __write_out_file(self):
        with codecs.open(self.out_filename, 'w', 'utf-8') as out:
            out.write(json.dumps(self.lists_parsed))
        self.logger.info("Word list data output to " + self.out_filename)

    def process(self, src_filename: str(), basic_list_no=1, sort=False):
        """Pre-process word list file, output as json"""
        self.__process_filename(src_filename)
        self.__open_src_file()
        self.__parse_src_file(basic_list_no, sort)
        self.__write_out_file()
        return self.out_filename
    
    def clean(self):
        os.remove(self.out_filename)