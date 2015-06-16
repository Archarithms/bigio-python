__author__ = 'Andrew Trimble'

import logging
import sys

logger = logging.getLogger(__name__)


def run(bigio):
    while True:
        print('bigio > ', end='', flush=True)
        cmd = sys.stdin.readline().rstrip()
        if cmd == 'quit':
            bigio.shutdown()
        elif cmd == 'whoami':
            logger.info(bigio.cluster.me)
        elif cmd == 'members':
            for member in bigio.cluster.member_holder.get_active_members():
                logger.info(member)
