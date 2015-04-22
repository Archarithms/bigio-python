__author__ = 'atrimble'

import logging
import signal
import sys
from cluster import Cluster

logging.basicConfig(format='%(asctime)s %(name)s - %(levelname)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S', level=logging.DEBUG)

logger = logging.getLogger(__name__)

cluster = None


class Speaker:
    def shutdown(self, signal=None, frame=None):
        global cluster
        logger.info('Closing connections')
        cluster.shutdown()
        logger.info('Goodbye')
        sys.exit(0)


    def initialize(self):
        global cluster
        global running

        cluster = Cluster()
        cluster.initialize()
        logger.info('Welcome to BigIO')

        signal.signal(signal.SIGINT, self.shutdown)
        signal.signal(signal.SIGTERM, self.shutdown)

        while True:
            input = sys.stdin.readline().rstrip()
            if input == 'quit':
                self.shutdown()


if __name__ == "__main__":
    speaker = Speaker()
    speaker.initialize()
