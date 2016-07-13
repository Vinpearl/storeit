#! /usr/bin/env python3

import os, sys, random

path = '.' if len(sys.argv) == 1 else sys.argv[1]

def walk_entry(indent, entry, path):
    walk(indent, entry.name, entry.stat().st_mtime, entry.is_dir(), path)

def walk(indent, name, st_mtime, is_dir, path):

    def printind(indent, msg):
        print('{}{}'.format(' ' * indent, msg))

    def print_entry(indent, st_mtime, is_dir, path):
        printind(indent, '{')
        indent += 2

        kind = ('0' if is_dir else '1')
        if kind == '1':
            path = path[:-1]

        printind(indent, '"path": "{}",'.format(path))
        printind(indent, '"metadata": "{}",'.format(int(st_mtime)))
        printind(indent, '"unique_hash": "{}",'.format(random.randrange(0, 10000000)))
        printind(indent, '"kind": ' + kind + ',')
        printind(indent, '"files": {')

        if is_dir:

            passed = False
            for entry in os.scandir(path):
                if passed:
                    printind(indent + 2, ',')
                printind(indent + 2, '"' + entry.name + '":')
                walk_entry(indent + 2, entry, path)
                passed = True

        printind(indent, '}')
        indent -= 2
        printind(indent, '}')

    path += name + '/'

    print_entry(indent, st_mtime, is_dir, path)

walk(0, '', 0, True, path)
