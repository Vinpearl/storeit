import asyncio
import traceback
from common.log import logger


class Network(asyncio.Protocol):

    data_buffer = bytes()
    incoming_bytes = 0

    def connection_made(self, transport):
        self.transp = transport

    def connection_lost(self, ext):
        logger.info('connection with peer was lost')

    # TODO: implement the fact that a command could be split in multiple data
    def data_received(self, data):

        def parse(cmd, size, args):
            self.parse_cmd(cmd, size, args, self.transp)

        if self.incoming_bytes > 0:
            self.data_buffer += data
            self.incoming_bytes -= len(data)
            logger.debug("waiting for {}".format(self.incoming_bytes))
            if self.incoming_bytes <= 0:
                if self.incoming_bytes < 0:
                    logger.warn("incoming_bytes should not be less than zero")
                self.incoming_bytes = 0
                parse(b'CSTR', 0, self.data_buffer)
                self.data_buffer = bytes()

        else:
            bytes_left = data
            while len(bytes_left) > 0:
              parsed = bytes_left.split(b' ', 2)
              if len(parsed) < 2:
                  logger.warn('invalid command {}'.format(bytes_left))
                  return

              cmd = parsed[0]
              size = parsed[1]
              args = parsed[2]
              # TODO: handle other commands as well
              size_int = int(size.decode())
              if cmd == b'CSTR' and size_int > len(args):
                  self.data_buffer = args
                  self.incoming_bytes = size_int - len(self.data_buffer)
                  break
              else:
                args_temp = args[:size_int]
                bytes_left = args[size_int:]
                args = args_temp
                try:
                    parse(cmd, size, args)
                except Exception as e:
                    logger.error(e)
                    for l in traceback.format_tb(e.__traceback__):
                        logger.error(l)


class NetworkServer(Network):
    pass

class NetworkClient(Network):
    pass

def loop(protocol_factory, ip, port):

    loop = asyncio.get_event_loop()

    # Each client connection will create a new protocol instance
    coro = loop.create_server(protocol_factory, ip, port)
    try:
        server = loop.run_until_complete(coro)

        # Serve requests until Ctrl+C is pressed
        logger.info('Serving on {}'.format(server.sockets[0].getsockname()))
        loop.run_forever()
    except Exception:
        logger.debug("something happened")

    try:
        # Close the server
        server.close()
        loop.run_until_complete(server.wait_closed())
        loop.close()

    except KeyboardInterrupt:
        logger.warn('keyboard interrupt')
        exit(1)
