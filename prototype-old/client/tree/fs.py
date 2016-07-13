from watchdog.events import FileSystemEventHandler
import chunk
import tree
import protocol
from common.log import logger

ignore_path = str()

class WatchFs(FileSystemEventHandler):

    def process(self, event):

        if event.event_type == 'modified':
            cmd = 'FUPT'
        elif event.event_type == 'created':
            cmd = 'FADD'
        elif event.event_type == 'deleted':
            protocol.send_FDEL(event.src_path)
            return
        else:
            logger.error('unknown event happening {}'.format(event))
            return

        if event.is_directory:
            return

        if event.src_path == ignore_path:
            return

        concerned = tree.produce_tree(False, event.src_path)
        chunk.register_tree(concerned)
        protocol.send_FCMD(cmd, concerned)

    def dispatch(self, event):
        self.process(event)

    def on_modified(self, event):
        self.process(event)

    def on_created(self, event):
        self.process(event)

    def on_moved(self, event):
        self.process(event)

    def on_deleted(self, event):
        self.process(event)
