import logging
import colorlog


def init_logging():
    formatter = colorlog.ColoredFormatter()

    ch = logging.StreamHandler()

    formatter = colorlog.ColoredFormatter(
    "%(log_color)s%(levelname)-8s%(reset)s %(blue)s%(message)s",
    datefmt=None,
    reset=True,
    log_colors={
    'DEBUG':    'cyan',
    'INFO':     'green',
    'WARNING':  'yellow',
    'ERROR':    'red',
    'CRITICAL': 'red,bg_white',
    },
    secondary_log_colors={},
                 style='%'
    )

    ch.setFormatter(formatter)

    logger = logging.getLogger('storeit')
    logger.addHandler(ch)
    logger.setLevel(logging.DEBUG)
    return logger

logger = init_logging()


def nomore(s):
    MAX = 80

    if len(str(s)) > MAX:
        appended = ' [...]'

        if isinstance(s, bytes):
            appended = appended.encode()
        else: 
            s = str(s)
        return s[:MAX] + appended

    return s
