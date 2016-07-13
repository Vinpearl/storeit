import tree
import chunk
import json
import hashlib
import network
import traceback

from common import log
from common.log import logger


def parse(cmd, size, args):

    class Command:

        def __init__(self, fcall, isstr):
            self.function_call = fcall
            self.is_string = isstr

    cmds = {b'FADD': Command(FADD, True),
            b'FUPT': Command(FUPT, True),
            b'CSND': Command(CSND, True),
            # TODO: rethink the hole stuff
            b'CSTR': Command(CSTR, False),
            b'CDEL': Command(CDEL, True)}

    logger.debug('somebody sent {} with args {}'.format(cmd, log.nomore(args)))
    cmds[cmd].function_call(args)


def CDEL(params):

    chk = params.decode()

    chunk.remove_chunk(chk)


def send_FCMD(name, tree):

    # FIXME: remove this quickfix
    if json.dumps(tree).find('DS_Store') != -1:
        return

    network.send_cmd('{} {}'.format(name, json.dumps(tree)))


def send_FDEL(path):
    network.send_cmd('FDEL {}'.format(path))


def FADD(params):

    params = params.decode()

    tr = json.loads(params)
    tree.make_file(tr)


def FUPT(params):
    pass


def CSND(params):

    params = params.decode()

    send, hsh, addr = params.split(' ', 2)

    ip, port = addr.split(':')
    if send == '1':
        logger.info('sending chunk {} to {} on port {}'.format(hsh, ip, port))
        send_CSTR(ip, int(port), hsh)
    else:
        logger.info('getting chunk {} from {}'.format(hsh, ip))
        pass  # TODO


def CSTR(data):

    logger.debug('CSTR for {} bytes'.format(len(data), data))

    # TODO: store only if we are waiting for it
    hasher = hashlib.sha256()
    hasher.update(data)
    chk = hasher.hexdigest()

    if chk in chunk.chunk_awaiting:
        with open(chunk.chunk_awaiting[chk], "wb") as file:
            file.write(data)
        del chunk.chunk_awaiting[chk]
    else:
        chunk.store_chunk(chk, data)


def send_CSTR(ip, port, hsh):

    path = chunk.get_path_for_chunk(hsh)

    if path is None:
        logger.error('chunk {} could not be found'.format(hsh))

    try:
        data = open(path, 'rb').read()
    except:
        logger.error('cannot read file {}'.format(path))
        return

    if data is None:
        logger.error('file read returned None')
        return

    network.send_payload(ip, port, data)


def login(client):

    json_tree = tree.usertree
    my_chks = list(chunk.my_chunks.keys())
    my_store = []  # TODO: later read the content of .store

    hashes = 'None' if len(my_chks) == 0 else ':'.join(my_chks + my_store)
  
    try:
      network.send_cmd('JOIN {} {} {} {}'
          .format(client.username, client.port,
            hashes, json.dumps(json_tree)))
    except Exception as e:
        logger.error('2: {} was raised'.format(log.nomore(e)))
        for l in traceback.format_tb(e.__traceback__):
            logger.debug(l)
        raise e
