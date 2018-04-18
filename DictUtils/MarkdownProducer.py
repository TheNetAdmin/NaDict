
import json
import os
import logging
import codecs
import textwrap

MD_MARCO = {
    'list_begin': '|word|translation|\n|-:|:-|\n',
    'list_title_prev': '||**LIST ',
    'list_title_after': '**|\n',
    'list_entry_separator': '|',
    'list_entry_endline': '|\n'
}

class MarkdownProducer(object):
    def __init__(self):
        self.src_filename = ''
        self.out_filename = ''
        self.src_file = None
        self.out_file = str()
        self.logger = logging.getLogger('UTILS.MarkdownProducer')
        self.curr_list_no = 0
        self.no_list = False
        self.words = list()

    def __process_filename(self, src_filename: str()):
        src_filename = os.path.abspath(src_filename)
        dir_name = os.path.dirname(src_filename)
        base_name = os.path.basename(src_filename)
        base_name = os.path.splitext(base_name)[0]
        self.src_filename = src_filename
        self.out_filename = os.path.join(dir_name, base_name + '.md')

    def __open_src_file(self):
        with codecs.open(self.src_filename, 'r', 'utf-8') as src:
            self.src_file = src.read()

    def __parse_src_file(self):
        self.words = json.loads(self.src_file)

    def __list_entry(self, word: dict()):
        entry = str()
        # add list title
        if self.no_list is False:
            if word['list_no'] != self.curr_list_no:
                self.curr_list_no = word['list_no']
                entry += MD_MARCO['list_title_prev']
                entry += str(self.curr_list_no)
                entry += MD_MARCO['list_title_after']
        # add original word
        entry += MD_MARCO['list_entry_separator']
        entry += word['data']['query']
        entry += MD_MARCO['list_entry_separator']
        # add explains
        if 'basic' in word['data'].keys():
            entry += ';'.join(word['data']['basic']['explains'])
        else:
            entry += ';'.join(word['data']['translation'])
        # add endline
        entry += MD_MARCO['list_entry_endline']
        self.logger.info("Added word [" + word['data']['query'] + ']')
        return entry

    def __perpare_md_file(self):
        self.out_file += '# Words \n\n'
        self.out_file += MD_MARCO['list_begin']
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
        self.__perpare_md_file()
        self.__write_out_file()
        self.logger.info("Markdown file generated: " + self.out_filename)