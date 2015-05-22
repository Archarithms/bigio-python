__author__ = 'atrimble'


def get_key(member=None, ip=None, gossip_port=None, data_port=None):
    """

    :param member:
    :param ip:
    :param gossip_port:
    :param data_port:
    :return:
    """
    if member is not None:
        return str(member.ip) + ':' + str(member.gossip_port) + ':' + str(member.data_port)
    elif ip is not None and gossip_port is not None and data_port is not None:
        return str(ip) + ':' + str(gossip_port) + ':' + str(data_port)
    return ''
