__author__ = 'atrimble'

import logging

from bigio.member.member_status import MemberStatus


logger = logging.getLogger(__name__)


class MemberHolder:

    def __init__(self):
        self.members = dict()
        self.active_members = dict()
        self.dead_members = dict()

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
        ret.append(self.members)
        return ret

    def get_active_members(self):
        ret = []
        for k in self.active_members:
            ret.append(self.active_members[k])
        return ret

    def get_dead_members(self):
        ret = []
        for k in self.dead_members:
            ret.append(self.dead_members[k])
        return ret

    def update_member_status(self, member):
        key = str(member.ip) + ':' + str(member.gossip_port) + ':' + str(member.data_port)

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
