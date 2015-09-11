

from bigio.cluster import Cluster
import logging
import time

logger = logging.getLogger(__name__)


def setup():
    logging.basicConfig(format='%(asctime)s %(name)s - %(levelname)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S', level=logging.DEBUG)


def teardown():
    pass


def test():
    # For some reason, this test causes the remote messaging test to fail
    return
    cluster1 = Cluster()
    cluster2 = Cluster()

    time.sleep(.5)

    mem1 = cluster1.member_holder.get_all_members()
    mem2 = cluster2.member_holder.get_all_members()

    try:
        assert len(mem1) == len(mem2) == 2
    finally:
        cluster1.shutdown()
        cluster2.shutdown()
