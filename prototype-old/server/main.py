#! /usr/bin/env python3

import database
import subprocess
import network
import logging
import time
from common.log import logger
import common.network
import argparse

logfile = '/tmp/storeit-server.log'

parser = argparse.ArgumentParser(description='StoreIt backend server.')
parser.add_argument('-l', '--log', nargs='?', const=logfile,
                    help='log to a file (default is {})'.format(logfile))

args = parser.parse_args()

if args.log is not None:
    logging.basicConfig(filename=args.log, level=logging.DEBUG)

try:
    database.__init__()
    database.find_user('nonexistent', 'user')
except Exception:
    logger.warn('Looks like postgre daemon is not running. It will be started')
    subprocess.call("./database/postgre.sh")
    time.sleep(0.2)
    database.__init__()

try:
    common.network.loop(network.NetManager, '0', 7641)
except Exception:
    logger.error("exception")
