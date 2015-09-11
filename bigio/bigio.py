__author__ = 'atrimble'

import logging
import threading
import signal
import sys
import bigio.cli as cli
from bigio.cluster import Cluster

logging.basicConfig(format='%(asctime)s %(name)s - %(levelname)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S', level=logging.DEBUG)

logger = logging.getLogger(__name__)

cluster = None


class BigIO:

    def __init__(self):
        self.cluster = Cluster()
        logger.info('Welcome to BigIO')

        signal.signal(signal.SIGINT, self.shutdown)
        signal.signal(signal.SIGTERM, self.shutdown)

        cli_thread = threading.Thread(target=cli.run, args=(self,))
        cli_thread.daemon = True
        cli_thread.start()

    def shutdown(self, signal=None, frame=None):
        logger.info('Closing connections')
        cli.stop()
        self.cluster.shutdown()
        logger.info('Goodbye')
        #sys.exit(0)

    def send(self, message, topic, partition=None, offset=None):
        self.cluster.send(message, topic, partition, offset)

    def add_listener(self, topic, listener, partition=None):
        self.cluster.add_listener(topic, listener, partition)

    def add_interceptor(self, topic, interceptor):
        self.cluster.add_interceptor(topic, interceptor)


if __name__ == "__main__":
    bigio = BigIO()
    bigio.initialize()
