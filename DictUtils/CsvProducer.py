
import json
import os
import logging
import codecs
import textwrap


class CsvProducer(object):
    def __init__(self):
        self.src_filename = ''
        self.out_filename = ''
        self.src_file = None
        self.out_file = str()
        self.logger = logging.getLogger('UTILS.CsvProducer')
        self.curr_list_no = 0
        self.no_list = False
        self.words = list()

    def __process_filename(self, src_filename: str()):
        src_filename = os.path.abspath(src_filename)
        dir_name = os.path.dirname(src_filename)
        base_name = os.path.basename(src_filename)
        base_name = os.path.splitext(base_name)[0]
        self.src_filename = src_filename
        self.out_filename = os.path.join(dir_name, base_name + '.csv')

    def __open_src_file(self):
        with codecs.open(self.src_filename, 'r', 'utf-8') as src:
            self.src_file = src.read()

    def __parse_src_file(self):
        self.words = json.loads(self.src_file)

    def __list_entry(self, word: dict()):
        entry = str()
        # add original word
        entry += word['data']['query'] + ','
        # add explains
        if 'basic' in word['data'].keys():
            explains = word['data']['basic']['explains']
        else:
            explains = word['data']['translation']
        for exp in explains:
            exp.replace(',', '，')
            exp.replace(' ','')
        entry += '；'.join(explains)
        # add endline
        entry += '\n'
        self.logger.info("Added word [" + word['data']['query'] + ']')
        return entry

    def __perpare_csv_file(self):
        for word in self.words:
            self.out_file += self.__list_entry(word)
    
    def __write_out_file(self):
        with codecs.open(self.out_filename, 'w', 'utf-8') as out:
            out.write(self.out_file)

    def loads(self, src_filename: str(), no_list: bool):
        """Load source json file and generate Latex file"""
        self.no_list = no_list
        self.__process_filename(src_filename)
        self.__open_src_file()
        self.__parse_src_file()
        self.__perpare_csv_file()
        self.__write_out_file()
        self.logger.info("Markdown file generated: " + self.out_filename)