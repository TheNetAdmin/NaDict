"""Imcremental words lookup & add producer"""
import codecs
import os


class IncProducer(object):
    def __init__(self):
        self.filename = str()
        self.words = list()
        self.section_no = input("Section NO.: ")

    def __del__(self):
        print('All words:\n')
        print(' '.join(self.words))
        if self.words is not None:
            with codecs.open(self.filename, 'a', 'utf-8') as file:
                file.write('\n---' + self.section_no + '\n')
                file.write(' '.join(self.words))

    def produce(self, filename: str(), dictionary):
        self.filename = filename
        word = str()
        explain = str()
        while True:
            os.system('clear')
            word = input('Word: ')
            if word == 'exit':
                break
            explain = dictionary.look_up(word)
            for trans in explain['translation']:
                print(trans)
            if 'basic' in explain.keys():
                for exp in explain['basic']['explains']:
                    print(exp)
            confirm = input('Add?[Y/n]: ')
            if confirm != 'n' and confirm != 'N':
                if word not in self.words:
                    self.words.append(word)
