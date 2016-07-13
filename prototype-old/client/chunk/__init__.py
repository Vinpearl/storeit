import tree
import os

from common.log import logger

chunk_awaiting = dict()
my_chunks = dict()


def register_chunk(chk: str, path: str):
    my_chunks[chk] = path


def register_tree(file_tree):

    if file_tree['kind'] != 0:
        register_chunk(file_tree['unique_hash'], file_tree['path'])
        return

    for f in file_tree['files'].values():
        if f['kind'] == 0:
            register_tree(f)
        else:
            register_chunk(f['unique_hash'], f['path'])


def register_chunks_from_tree():
    # TODO: find a better hack
    if tree.usertree is None:
        tree.usertree = tree.produce_tree()

    register_tree(tree.usertree)

register_chunks_from_tree()


def wait_for_chunk(chk: str, path: str):
    logger.debug('waiting for chunk {} ({})'.format(chk, path))
    chunk_awaiting[chk] = path

store_name = None


def get_path_for_chunk(hsh):
    if hsh not in my_chunks:
        if os.path.exists(store_name + hsh):
            return store_name + hsh
        logger.error('chunk {} does not exists'.format(hsh))
        return None
    return my_chunks[hsh]


def store_chunk(chk, data: bytes):
    if not os.path.exists(store_name):
        os.makedirs(store_name)

    with open(store_name + chk, "wb") as file:
        file.write(data)
        logger.debug("chunk written in {}".format(store_name + chk))


def remove_chunk(chk):
    logger.debug('remove chunk: TODO')
