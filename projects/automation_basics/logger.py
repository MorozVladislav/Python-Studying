import logging
import sys
import pdb
import os


LOG_DIR = os.getcwd() + '/logs/'
LOGGERS = {}


def get_logger(name=None, level=logging.INFO, filename=None):
    if name in LOGGERS:
        return LOGGERS[name]

    if not os.path.exists(LOG_DIR):
        os.mkdir(LOG_DIR)

    logger = logging.getLogger(name=name)
    logger.setLevel(level)
    f = logging.Formatter(fmt='[%(levelname)s] %(asctime)s %(filename)s.%(funcName)s: %(message)s')
    sh = logging.StreamHandler(stream=sys.stdout)
    sh.setFormatter(f)
    logger.addHandler(sh)
    logfile = filename or name or 'logs'
    fh = logging.FileHandler(filename=LOG_DIR + logfile + '.log')
    fh.setFormatter(f)
    logger.addHandler(fh)
    LOGGERS[name] = logger

    return logger


log = get_logger(__name__)


if __name__ == '__main__':
    # pdb.set_trace()
    log.debug('Debug message')
    log.info('Info message')
    log.warning('Warning message')
