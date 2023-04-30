import logging

def get_logger(name):
    name = name.replace(__name__.split('.')[0], 'openlavaserver')
    return logging.getLogger(name)


logger = get_logger(__name__)