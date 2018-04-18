"""Produce latex files and generate pdf"""

import json
import os
import logging
import codecs
import textwrap

LATEX_MARCO = {
    'tex_header': """
                  \\documentclass[a4paper,5pt]{book}
                  \\usepackage[UTF8]{ctex}
                  \\usepackage{geometry}
                  \\geometry{left=1cm, right=1cm, top=1cm, bottom=2cm}
                  \\usepackage{tabularx}
                  \\usepackage{ltablex}
                  \\usepackage{multirow}
                  \\usepackage[explicit]{titlesec}
                  \\titleformat{\\chapter}[drop]{}{}{0pt}{}
                  \\titlespacing*{\\chapter}{0pt}{0pt}{0pt}
                  """,
    'doc_begin': '\\begin{document}\n\n',
    'doc_end': '\\end{document}\n',
    'list_begin': '\\begin{tabularx}{\\linewidth}{|r|X|} \\hline \n',
    'simple_list_begin': '\\begin{tabularx}{\\linewidth}{|X|X|X|X|X|X|} \\hline \n',
    'simple_list_end': '\\end{tabularx}\n\n',
    'list_end': '\\end{tabularx}\n\n',
    'list_title_prev': '\\multicolumn{2}{|c|}{\\multirow{2}*{\\textbf{LIST ',
    'list_title_after': '}}} \\\\ \\multicolumn{2}{|c|}{~} \\\\ \\hline \n',
    'list_entry_separator': ' & ',
    'list_entry_endline': '\\\\ \\hline \n',
    'page_break': '\\newpage \n'
}


class LatexProducer(object):
    """Produce latex files, generate pdf"""

    def __init__(self):
        self.src_filename = ''
        self.out_filename = ''
        self.src_file = None
        self.out_file = str()
        self.logger = logging.getLogger('UTILS.LatexProducer')
        self.curr_list_no = 0
        self.words = list()
        self.no_list = False
        self.simple_entry_num = 0

    def __process_filename(self, src_filename: str()):
        src_filename = os.path.abspath(src_filename)
        dir_name = os.path.dirname(src_filename)
        base_name = os.path.basename(src_filename)
        base_name = os.path.splitext(base_name)[0]
        self.src_filename = src_filename
        self.out_filename = os.path.join(dir_name, base_name + '.tex')

    def __open_src_file(self):
        with codecs.open(self.src_filename, 'r', 'utf-8') as src:
            self.src_file = src.read()

    def __parse_src_file(self):
        self.words = json.loads(self.src_file)

    def __list_entry(self, word: dict()):
        entry = '\t'
        # add list title
        if self.no_list is False:
            if word['list_no'] != self.curr_list_no:
                self.curr_list_no = word['list_no']
                entry += LATEX_MARCO['list_title_prev']
                entry += str(self.curr_list_no)
                entry += LATEX_MARCO['list_title_after']
                entry += '\t'
        # add original word
        entry += word['data']['query']
        entry += LATEX_MARCO['list_entry_separator']
        # add explains
        try:
            if 'basic' in word['data'].keys():
                entry += ';'.join(word['data']['basic']['explains'])
            else:
                entry += ';'.join(word['data']['translation'])
        except KeyError:
            self.logger.error('Word ['+word['data']['query'] +'] has no translation')
            exit(1)
        # add endline
        entry += LATEX_MARCO['list_entry_endline']
        self.logger.info("Added word [" + word['data']['query'] + ']')
        return entry

    def __add_simple_entry(self, word: str()):
        self.simple_entry_num += 1
        entry = str()
        entry += word
        if self.simple_entry_num % 6 == 0:
            entry += LATEX_MARCO['list_entry_endline']
            entry += '\t'
        else:
            entry += LATEX_MARCO['list_entry_separator']
        return entry

    def __fill_simple_line(self):
        out = str()
        while self.simple_entry_num % 6 != 0:
            out += self.__add_simple_entry('~')
        return out

    def __simple_list(self):
        out = str()
        last_list_no = 0
        for word in self.words:
            if word['list_no'] != last_list_no:
                last_list_no = word['list_no']
                out += self.__fill_simple_line()
                out += self.__add_simple_entry('\\textbf{List ' + str(word['list_no']) + '}')
            out += self.__add_simple_entry(word['data']['query'])
        out += self.__fill_simple_line()
        return out

    def __prepare_latex_file(self):
        self.out_file += textwrap.dedent(LATEX_MARCO['tex_header'])
        self.out_file += LATEX_MARCO['doc_begin']
        self.out_file += '\\chapter{Words}\n'
        self.out_file += LATEX_MARCO['simple_list_begin']
        self.out_file += self.__simple_list()
        self.out_file += LATEX_MARCO['simple_list_end']
        self.out_file += LATEX_MARCO['page_break']
        self.out_file += '\\chapter{Explains}\n'
        self.out_file += LATEX_MARCO['list_begin']
        for word in self.words:
            self.out_file += self.__list_entry(word)
        self.out_file += LATEX_MARCO['list_end']
        self.out_file += LATEX_MARCO['doc_end']

    def __write_out_file(self):
        with codecs.open(self.out_filename, 'w', 'utf-8') as out:
            out.write(self.out_file)

    def loads(self, src_filename: str(), no_list: bool):
        """Load source json file and generate Latex file"""
        self.no_list = no_list
        self.__process_filename(src_filename)
        self.__open_src_file()
        self.__parse_src_file()
        self.__prepare_latex_file()
        self.__write_out_file()
        self.logger.info("Latex file generated: " + self.out_filename)

    def generate_pdf(self):
        """Compile Latex to pdf"""
        # Change to out file dir
        curr_dir_name = os.getcwd()
        os.chdir(os.path.dirname(self.out_filename))
        # Compile to pdf
        out_base_filename = os.path.basename(self.out_filename)
        os.system('latexmk -xelatex -quiet ' + out_base_filename)
        # Leave out file dir
        os.chdir(curr_dir_name)
        self.logger.info("Pdf file generated")

    def clean(self):
        """Clean aux files generated by latexmk, preserve pdf file"""
        # Change to out file dir
        curr_dir_name = os.getcwd()
        os.chdir(os.path.dirname(self.out_filename))
        # Clean aux files, preserve pdf file
        out_base_filename = os.path.basename(self.out_filename)
        out_base_filename_noext = os.path.splitext(out_base_filename)[0]
        os.rename(out_base_filename_noext + '.pdf', 'temp')
        os.system('latexmk -CA -quiet ' + out_base_filename)
        os.remove(self.out_filename)
        os.rename('temp', out_base_filename_noext + '.pdf')
        # Leave out file dir
        os.chdir(curr_dir_name)
        self.logger.info("Aux files cleaned")