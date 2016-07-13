import asyncio
import protocol
import threading
import socket
import traceback
from common import log

from common.network import NetworkServer
from common.network import NetworkClient

from common.log import logger

server_transport = None
receivers = list()
server_addr = str()
server_port = int()

class Receiver():

    def __init__(self, transport):
        self.transport = transport


class Network():

    data_buffer = bytes()

    def data_received(self, data):
        self.data_buffer += data


class Server(NetworkServer):

    def connection_made(self, transport):
        receivers.append(Receiver(transport))
        NetworkServer.connection_made(self, transport)

    def parse_cmd(self, cmd, size, args, transp):
        protocol.parse(cmd, size, args)


class Client(NetworkClient):

    def __init__(self, loop, port, username):
        self.loop = loop
        self.byte_count = 0
        self.username = username
        self.port = port
        NetworkClient.__init__(self)

    def connection_made(self, transp):
        
        NetworkClient.connection_made(self, transp)

        global server_transport

        logger.info("connected to master server")
        server_transport = transp

        try:
            protocol.login(self)
        except Exception as e:
            logger.error(e)
            logger.error('{} was raised'.format(log.nomore(e)))
            for l in traceback.format_tb(e.__traceback__):
                logger.debug(l)
            raise e

    def parse_cmd(self, cmd, size, args, transp):
        protocol.parse(cmd, size, args)

    def connection_lost(self, exc):
        NetworkClient.connection_lost(self, exc)
        self.loop.stop()


def format_cmd(data):
    return data[:5] + bytes(str(len(data) - 5) + ' ', 'ascii') + data[5:]


def send_cmd(msg):

    if type(msg) is str:
        msg = msg.encode()

    final_cmd = format_cmd(msg)
    logger.debug('sending: {}'.format(log.nomore(final_cmd)))
    server_transport.write(final_cmd)


def listen(port):
    eloop = asyncio.new_event_loop()
    asyncio.set_event_loop(eloop)

    coro = eloop.create_server(Server, '0.0.0.0', port)
    server = eloop.run_until_complete(coro)

    logger.info('listening on {}'.format(server.sockets[0].getsockname()))
    try:
        eloop.run_forever()
    except KeyboardInterrupt:
        logger.warn('keyboard interrupt')
        pass

    server.close()
    eloop.run_until_complete(server.wait_closed())
    eloop.close()


def loop(client_port, username):
    thread = threading.Thread(target=listen, args=(client_port,))
    thread.daemon = True
    thread.start()

    loop = asyncio.get_event_loop()
    coro = loop.create_connection(lambda: Client(loop, client_port, username), server_addr, server_port)
    try:
        loop.run_until_complete(coro)
        loop.run_forever()
    except KeyboardInterrupt:
        logger.warn('keyboard interrupt')
        pass

    loop.close()


def send_payload(ip, port, data):

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((ip, port))

    final = format_cmd(b'CSTR ' + data)
    logger.debug('sending: {}'.format(log.nomore(final)))
    sock.send(final)
