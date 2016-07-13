#! /usr/bin/env python3

import os
import hashlib
import json

usertree = None
root = './storeit/'


def hashfile(afile, hasher, blocksize=65536):
    buf = afile.read(blocksize)
    while len(buf) > 0:
        hasher.update(buf)
        buf = afile.read(blocksize)
    return hasher.hexdigest()


def compute_hash_for_file(path):

    # TODO: recursive if it is a directory
    if os.path.isdir(path):
        return 42
    return hashfile(open(path, 'rb'), hashlib.sha256())


def walk_entry(indent, entry, path):
    return walk(indent, entry.name, entry.stat().st_mtime, entry.is_dir(), path)


def walk(indent, name, st_mtime, is_dir, path):
    def printind(indent, msg):
        return '{}{}\n'.format(' ' * indent, msg)

    def print_entry(indent, st_mtime, is_dir, path):
        result = str()
        result += printind(indent, '{')
        indent += 2

        kind = ('0' if is_dir else '1')
        if kind == '1':
            path = path[:-1]

        result += printind(indent, '"path": "{}",'.format(path))
        result += printind(indent, '"metadata": "{}",'.format(int(st_mtime)))
        hsh = 0 if kind == '0' else compute_hash_for_file(path)
        result += printind(indent, '"unique_hash": "{}",'.format(hsh))
        result += printind(indent, '"kind": ' + kind + ',')
        result += printind(indent, '"files": {')

        if is_dir:

            passed = False
            for entry in os.scandir(path):
                # FIXME: ugly quickfix
                if entry.name[0] == '.' and entry.name[1] != '/':
                    print('dismissing {}'.format(entry.name))
                    continue
                if passed:
                    result += printind(indent + 2, ',')
                result += printind(indent + 2, '"' + entry.name + '":')
                result += walk_entry(indent + 2, entry, path)
                passed = True

        result += printind(indent, '}')
        indent -= 2
        result += printind(indent, '}')

        return result

    path += name + '/'

    return print_entry(indent, st_mtime, is_dir, path)


def produce_tree(is_dir=True, _root=root):
    return json.loads(walk(0, '', 0, is_dir, _root))

import chunk

from tree import fs

# possible security/bug issue. Add checks on what we create
def make_file(tree):

    path = tree['path']

    if tree['kind'] == 0:
        if not os.path.exists(path):
            os.makedirs(path)
        for f in tree['files'].values():
            make_file(f)
    else:
        dirpath = os.path.dirname(path)
        if not os.path.exists(dirpath):
            os.makedirs(dirpath)
        fs.ignore_path = path
        with open(path, "w"):
            pass
        chunk.wait_for_chunk(tree['unique_hash'], tree['path'])

usertree = produce_tree()
