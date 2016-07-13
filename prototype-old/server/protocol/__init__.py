import shared
import engine
import database
import json
import chunk
from common.log import logger

last_transport = None


# JOIN username port file_json_object
def JOIN(client, data):

    data = data.decode()
    username, port, hashes, json = data.split(' ', 3)

    client = shared.climanager.add_cli(username, port, json, last_transport)

    if client is None:
        return False

    if hashes != 'None':
        chunk.add_user(client, hashes.split(':'))

    return True


def parse(cmd, size, args, transp):

    global last_transport
    last_transport = transp

    cmds = {b'JOIN': JOIN,
            b'FADD': FADD,
            b'FPDT': FUPT,
            b'FDEL': FDEL}

    if cmd not in cmds:
        logger.error('unknown command {}'.format(cmd))
        return

    client = None

    if transp in shared.climanager.transports:
        client = shared.climanager.transports[transp]

    if client is None and cmd != b'JOIN':
        logger.error("""no client has been found for this connection and """
                     """command {}. Refusing to continue""".format(cmd))

    # TODO: use size
    cmds[cmd](client, args)


def FDEL(client, args):
    logger.warn('unimplemented FDEL')
    pass


def FADD(client, args):
    logger.debug('fadd : {}'.format(args))
    tr = json.loads(args.decode())

    directory, filename = client.find_in_tree(tr)

    engine.FADD(directory, 'client', filename, tr, client)

    logger.info('new user tree has been saved for {}'.format(client.username))
    database.save_new_tree(client.username, client.user_tree.raw_tree)


def FUPT(client, args):
    tr = json.loads(args.decode())

    # TODO: catch exception
    # TODO: remove the unused chunk
    # TODO: don't use engine.FADD, find something more elegant

    directory, filename = client.find_in_tree(tr)

    engine.FADD(directory, 'client', filename, tr, client)


def send_FUPT(tree, client):
    if type(tree) == dict:
        tree = json.dumps(tree)

    client.send_cmd('FUPT {}'.format(tree))


def send_FADD(tree, client):
    if type(tree) == dict:
        tree_json = json.dumps(tree)

    client.send_cmd('FADD {}'.format(tree_json))
    # TODO: wait for response

    if tree['kind'] != 0:
        engine.send_chunk_to(client, tree['unique_hash'])


def send_CDEL(client, chk):
    client.send_cmd(b'CDEL ' + chk)


def send_CSND(from_cli, to_cli, send: int, chk: str):

    if to_cli.transport is None:
      logger.error("send_CSND: client has no transport")
      return

    addr = to_cli.transport.get_extra_info('peername')
    if addr is None:
        logger.error('could not get ip for user {}'.format(to_cli.username))

    addr_and_port = addr[0] + ':' + to_cli.port
    from_cli.send_cmd('CSND {} {} {}'
                      .format(send, chk, addr_and_port))
