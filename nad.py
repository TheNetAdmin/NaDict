"""NaDict: Not a Dictionary"""

import argparse
import logging
from Config.version import __version__
from DictUtils.Prep import Prep
from DictUtils.Translator import Translator
from DictUtils.LatexProducer import LatexProducer
from DictUtils.Loggers import logging_setup
from DictUtils.Dict import Dictionary
from DictUtils.MarkdownProducer import MarkdownProducer
from DictUtils.WordMode import WordMode
from DictUtils.CsvProducer import CsvProducer


def main():
    """Parse all args and process the translation"""
    # config logging
    logging_setup()

    # config args parser
    parser = argparse.ArgumentParser()
    optional_args = parser
    required_args = parser.add_argument_group('required arguments')
    # optional args
    optional_args.add_argument('-b', '--basic_list_no', type=int,
                               default=1, help='The start list number, default to 1')
    optional_args.add_argument('-v', '--version', action='version',
                               version='Dictionary {version}'.format(version=__version__))
    optional_args.add_argument('-l', '--latex', action='store_true',
                               help='Generate latex file and pdf')
    optional_args.add_argument('-m', '--markdown', action='store_true',
                               help='Generate markdown file')
    optional_args.add_argument('-n', '--no_list', action='store_true',
                               help='Do not generate list title')
    optional_args.add_argument('-c', '--clean', action='store_true',
                               help='Clean all intermediate files after all process')
    optional_args.add_argument('--sort', action='store_true',
                               help='Sort the word lists')
    optional_args.add_argument('-s', '--src_file_name',
                               help='Specify src file name')
    optional_args.add_argument('--csv', action='store_true',
                               help='Output csv file')
    optional_args.add_argument('-w', '--word_mode', action='store_true',
                               help='Enter word mode')
    # required args
    required_args.add_argument('-d', '--dict_file_name',
                               required=True, help='Specify dictionary file name')
    # parse args
    args = parser.parse_args()

    if args.word_mode:
        wm = WordMode()
        wm.start(args.dict_file_name, args.src_file_name)
    else:
        # config modules
        prep = Prep()
        translator = Translator()
        latex = LatexProducer()
        markdown = MarkdownProducer()
        csv = CsvProducer()
        dictionary = Dictionary(args.dict_file_name)

        # Start translation
        prep_out = prep.process(
            args.src_file_name, args.basic_list_no, args.sort)
        translate_out = translator.translate(prep_out, dictionary)
        if args.latex:
            latex.loads(translate_out, args.no_list)
            latex.generate_pdf()
            if args.clean:
                latex.clean()
        if args.markdown:
            markdown.loads(translate_out, args.no_list)
        if args.csv:
            csv.loads(translate_out, args.no_list)
        if args.clean:
            prep.clean()
            translator.clean()


if __name__ == '__main__':
    main()
