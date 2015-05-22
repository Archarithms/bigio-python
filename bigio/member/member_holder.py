__author__ = 'atrimble'

import logging

from bigio.member.member_status import MemberStatus
from bigio.util import utils
from threading import Lock


logger = logging.getLogger(__name__)


class MemberHolder:

    def __init__(self):
        self.members = dict()
        self.active_members = dict()
        self.dead_members = dict()
        self.lock = Lock()

    def clear(self):
        self.members.clear()
        self.active_members.clear()
        self.dead_members.clear()

    def get_member(self, key):
        if key in self.members:
            return self.members[key]
        else:
            return None

    def get_all_members(self):
        ret = []
        for k, v in self.members.items():
            ret.append(v)
        return ret

    def get_active_members(self):
        ret = []
        for k, v in self.active_members.items():
            ret.append(v)
        return ret

    def get_dead_members(self):
        ret = []
        for k, v in self.dead_members.items():
            ret.append(v)
        return ret

    def update_member_status(self, member):
        key = utils.get_key(member)

        self.lock.acquire()
        '''
        logger.info('**** Before')
        for k, v in self.members.items():
            logger.info(k)
        logger.info('****')
        '''

        if key in self.members:
            if key in self.active_members and (member.status == MemberStatus.Failed or member.status == MemberStatus.Left or member.status == MemberStatus.Unknown):
                self.active_members.pop(key)
                self.dead_members[key] = member
            elif key in self.dead_members and member.status == MemberStatus.Alive:
                self.dead_members.pop(key)
                self.active_members[key] = member
        else:
            logger.info('Adding new member at key ' + str(key))
            self.members[key] = member
            if MemberStatus.Alive == member.status:
                self.active_members[key] = member
            else:
                self.dead_members[key] = member

        '''
        logger.info('**** After')
        for k, v in self.members.items():
            logger.info(k)
        logger.info('****')
        '''

        self.lock.release()
