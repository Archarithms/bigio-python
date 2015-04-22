__author__ = 'atrimble'

from bigio.member.member_status import MemberStatus


class Member:
    ip = None
    status = MemberStatus.Unknown
    sequence = 0
    tags = dict()
    data_port = 0
    gossip_port = 0
    public_key = None