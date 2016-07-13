import protocol
import chunk
import shared
from common.log import logger
from common import hash


def FADD(directory, from_who, filename, tree, client):
    logger.debug('user {} adding {} from {}'
                 .format(client.username, tree['path'], from_who))

    if from_who == 'server':
        protocol.send_FADD(tree, client)
    elif tree['kind'] != 0:
        hsh = chunk.register_chunk(hash.Hash(tree['unique_hash']), client)
        chunk.keep_chunk_alive(client, hsh)

        for instance in shared.climanager.clients[client.username]:
            if instance is not client:
                FADD(directory, 'server', filename, tree, instance)
    else:
        pass  # TODO: handle adding a directory with some content

    directory[filename] = tree


def FUPT(new_tree, from_who, old_tree, client):
    if from_who == 'server':
        protocol.send_FUPT(new_tree, client)
        if new_tree['kind'] != 0:
            send_chunk_to(client, hash.Hash(new_tree['unique_hash']))

    if from_who == 'client' and old_tree['kind'] != 0:
        # FIXME: it will happen that some clients share identical chunks,
        # do not do this
        make_chunk_disappear(hash.Hash(old_tree['unique_hash']))
        chunk.keep_chunk_alive(client, hash.Hash(new_tree['unique_hash']))

    old_tree['unique_hash'] = new_tree['unique_hash']


def make_chunk_disappear(chk):

    chk = check_for_string(chk)

    owners = chunk.get_chunk_owners(chk)

    for o in owners:
        protocol.send_CDEL(o, chk)

    chunk.remove_chunk(chk)


def check_for_string(s):
    if type(s) != hash.Hash:
        return hash.Hash(s)

    return s


def send_chunk_to(client: hash.Hash, chk):
    chk = check_for_string(chk)

    from_cli = chunk.get_chunk_owner(chk)
    if from_cli is None:
        logger.warn('could not find any user hosting {}'.format(chk.pretty()))
        return

    logger.debug('{} is being sent from {} to {}'
                 .format(chk.pretty(), from_cli.username, client.username))
    protocol.send_CSND(from_cli, client, 1, chk)
    protocol.send_CSND(client, from_cli, 0, chk)
    chunk.register_chunk(chk, client)


def host_chunk(frm, chk):
    chk = check_for_string(chk)

    user = chunk.find_user_for_storing(chk)

    if user is None:
        logger.warn("""could not find any user to store {} (from {})."""
                    """Chunk currently has {} hosted instances"""
                    .format(chk.pretty(), frm.username, chunk.get_redundancy(chk)))
        return

    send_chunk_to(user, chk)
