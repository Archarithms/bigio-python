__author__ = 'atrimble'

import logging
from bigio.listener_registry import ListenerRegistry
from bigio.member.me_member import MeMember
from bigio.member.member_holder import MemberHolder
import bigio.util.utils as utils


logger = logging.getLogger(__name__)

me = None
registry = None


def intercept():
    pass


def listener():
    pass


def setup():
    global me, registry
    logging.basicConfig(format='%(asctime)s %(name)s - %(levelname)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S', level=logging.DEBUG)
    me = MeMember()
    holder = MemberHolder()
    holder.update_member_status(me)
    registry = ListenerRegistry(me, holder)


def teardown():
    pass


def test_interceptor():
    global me, registry
    registry.add_interceptor('test', intercept)
    assert 'test' in me.interceptors
    assert intercept in me.interceptors['test']


def test_local_listener():
    global me, registry
    registry.add_local_listener('topic1', listener)
    assert 'topic1' in me.data_reactor.handlers
    assert listener in me.data_reactor.handlers['topic1']


def test_register():
    global me, registry
    registry.register_member_for_topic('topic2', me)
    key = utils.get_key(me)
    assert key in registry.map
    assert 'topic2' in registry.map[key]
    assert len(registry.map[key]) == 1

    assert len(registry.get_registered_members('topic2')) == 1
    assert me in registry.get_registered_members('topic2')

    registry.remove_registration(me, 'topic2')
    assert 'topic2' not in registry.map[key]

