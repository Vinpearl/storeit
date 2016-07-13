"""Handle the chunk (stored/sent pieces of a file)."""

from common.log import logger
from common.hash import Hash
import shared
import engine

chunks = dict()
users = dict()


def add_user(who, hashes: list):

    logger.debug('{} has {} chunks to register'.
                 format(who.username, len(hashes)))

    for h in hashes:
        if h == '':
            logger.warn('{} sent invalid chunk hash'.format(who.username))
            continue
        h = Hash(h)
        register_chunk(h, who)
        keep_chunk_alive(who, h)


def get_chunk_owners(chk: Hash):
    if chk not in chunks:
        return []
    return chunks[chk]


# TODO: add an availability flag to know if the client is available
def get_chunk_owner(chk: Hash):
    if chk not in chunks or chunks[chk] == []:
        return None
    return list(chunks[chk])[0]  # FIXME: ugly, do dynamic


def has_user_chunk(chk, cli):
    if chk not in chunks:
        return []
    return cli in chunks[chk]


def register_chunk(chk, cli):

    logger.debug("registering chunk {} for {}".format(chk.pretty(), cli.username))

    if isinstance(chk, str):
        chk = Hash(chk)

    # TODO: use smart dict

    if chk not in chunks:
        chunks[chk] = {cli}
    else:
        chunks[chk].add(cli)

    if cli not in users:
        users[cli] = {chk}
    else:
        users[cli].add(chk)

    return chk


def remove_user(frm):

    if frm not in users:
        logger.debug('user {} has zero chunks'.format(frm.username))
        return

    for chk in users[frm]:
        chunks[chk].remove(frm)
        keep_chunk_alive(frm, chk)

    del users[frm]


def remove_chunk(chk):
    if chk not in chunks:
        logger.debug('chunk {} does not exists'.format(chk))
        return

    for cli in chunks[chk]:
        users[cli].remove(chk)

    del chunks[chk]


def get_redundancy(chk):

    if chk not in chunks:
        return 0
    return len(chunks[chk])


def dump():

    for user, chks in users.items():
        logger.debug('user {} has {}'
                     .format(user.username, tuple(c.pretty() for c in chks))) # TODO: use builtin istead of comprehension
    for chks, usrs in chunks.items():
        logger.debug('chk {} is owned by {}'.format(chks.pretty(), usrs))


def find_user_for_storing(chk: Hash):
    for user_instances in shared.climanager.clients.values():
        for instance in user_instances:
            if not has_user_chunk(chk, instance):
                return instance
    return None


def keep_chunk_alive(frm, chk: Hash):
    redundancy = get_redundancy(chk)

    REDUNDANCY_LEVEL = 3

    # TODO: do some multicast propagation for chunk hosting
    while redundancy < REDUNDANCY_LEVEL:
        engine.host_chunk(frm, chk)
        redundancy += 1
