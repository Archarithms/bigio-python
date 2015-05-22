__author__ = 'atrimble'

import logging
import signal
import sys
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

        while True:
            input = sys.stdin.readline().rstrip()
            if input == 'quit':
                self.shutdown()

    def shutdown(self, signal=None, frame=None):
        logger.info('Closing connections')
        self.cluster.shutdown()
        logger.info('Goodbye')
        sys.exit(0)

    def send(self, message, topic, partition=None, offset=None, java_class=None):
        self.cluster.send(message, topic, partition, offset, java_class)

    def add_listener(self, topic, listener, partition=None):
        self.cluster.add_listener(topic, listener, partition)

    def add_interceptor(self, topic, interceptor):
        self.cluster.add_interceptor(topic, interceptor)


if __name__ == "__main__":
    bigio = BigIO()
    bigio.initialize()
