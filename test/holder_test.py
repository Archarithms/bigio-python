__author__ = 'atrimble'

import logging
from bigio.member.me_member import MeMember
from bigio.member.member_status import MemberStatus
from bigio.member.member_holder import MemberHolder
import bigio.util.utils as utils


logger = logging.getLogger(__name__)

key = None
me = None
holder = None


def intercept():
    pass


def listener():
    pass


def setup():
    global me, key, holder
    logging.basicConfig(format='%(asctime)s %(name)s - %(levelname)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S', level=logging.DEBUG)
    me = MeMember()
    key = utils.get_key(me)
    holder = MemberHolder()


def teardown():
    pass


def test():
    global me, key, holder

    assert me.status == MemberStatus.Unknown
    holder.update_member_status(me)

    assert key in holder.members
    assert key in holder.dead_members
    assert key not in holder.active_members

    me.status = MemberStatus.Alive
    holder.update_member_status(me)

    assert key in holder.members
    assert key not in holder.dead_members
    assert key in holder.active_members

    me.status = MemberStatus.Left
    holder.update_member_status(me)

    assert key in holder.members
    assert key in holder.dead_members
    assert key not in holder.active_members

    me.status = MemberStatus.Failed
    holder.update_member_status(me)

    assert key in holder.members
    assert key in holder.dead_members
    assert key not in holder.active_members
