__author__ = 'Andrew Trimble'

import logging
import sys

logger = logging.getLogger(__name__)


running = True


def stop():
    global running
    running = False


def run(bigio):
    global running
    while running:
        print('bigio > ', end='', flush=True)
        cmd = sys.stdin.readline().rstrip()
        if cmd == 'quit':
            bigio.shutdown()
        elif cmd == 'whoami':
            logger.info(bigio.cluster.me)
        elif cmd == 'members':
            for member in bigio.cluster.member_holder.get_active_members():
                logger.info(member)
        elif cmd == 'listeners':
            for key, topic_list in bigio.cluster.listener_registry.get_all_registrations().items():
                logger.info(key + ' ->')
                for topic in topic_list:
                    logger.info('    ' + topic)
        elif cmd == 'help':
            logger.info('Commands:')
            logger.info('members   - list all the known active members')
            logger.info('whoami    - display information about this node')
            logger.info('listeners - list all known registered listeners')
            logger.info('quit      - exit the program')
            logger.info('help      - print this message')
        elif cmd != '':
            logger.info('Unrecognized command "' + cmd + '" - type "help" for a list of available commands.')
