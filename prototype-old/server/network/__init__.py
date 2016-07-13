import shared
import protocol
import common.network

from common.log import logger


class NetManager(common.network.NetworkServer):

    data_buffer = str()
    transp = None

    def connection_made(self, transport):
        common.network.NetworkServer.connection_made(self, transport)
        self.transp = transport

    def connection_lost(self, ext):
        try:
            username = shared.climanager.transports[self.transp]
            del shared.climanager.clients[username]
            del shared.climanager.transports[self.transp]
            logger.info('{} has disconnected'.format(username))
            NetManager.connection_lost(self, ext)
        except KeyError:
            logger.info('connection with some unidentified client lost')

    def parse_cmd(self, cmd, size, args, transport):
        protocol.parse(cmd, size, args, transport)
