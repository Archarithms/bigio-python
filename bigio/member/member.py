__author__ = 'atrimble'

from bigio.member.member_status import MemberStatus


class Member:
    def __init__(self):
        self.ip = None
        self.status = MemberStatus.Unknown
        self.sequence = 0
        self.tags = dict()
        self.data_port = 0
        self.gossip_port = 0
        self.public_key = None