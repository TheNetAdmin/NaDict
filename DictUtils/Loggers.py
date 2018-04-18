"""Config loggers"""
import logging

def logging_setup():
    """Config loggers"""
    # formatters
    standard_formatter = logging.Formatter('[DICT]: %(levelname)s - %(name)s: %(message)s')
    # handlers
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(standard_formatter)
    console_handler.setLevel(logging.INFO)
    # loggers
    # root
    root_logger = logging.getLogger('root')
    root_logger.setLevel(logging.INFO)
    root_logger.addHandler(console_handler)
    root_logger.propagate = False
    # Dict
    dict_logger = logging.getLogger('Dict')
    dict_logger.setLevel(logging.INFO)
    dict_logger.addHandler(console_handler)
    dict_logger.propagate = False
    # DictUtils
    dictutils_logger = logging.getLogger('UTILS')
    dictutils_logger.setLevel(logging.INFO)
    dictutils_logger.addHandler(console_handler)
    dictutils_logger.propagate = False