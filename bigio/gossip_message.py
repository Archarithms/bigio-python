__author__ = 'atrimble'


class GossipMessage:
    ip = None
    gossip_port = 0
    data_port = 0
    milliseconds_since_midnight = 0
    public_key = None
    tags = dict()
    members = []
    clock = []
    listeners = dict()

    def __str__(self):
        ret = '{\n'
        ret = ret + '  ip: "' + str(self.ip) + '",\n'
        ret = ret + '  gossip_port: "' + str(self.gossip_port) + '",\n'
        ret = ret + '  data_port: "' + str(self.data_port) + '",\n'
        ret = ret + '  milliseconds_since_midnight: "' + str(self.milliseconds_since_midnight) + '",\n'
        ret = ret + '  public_key: "' + str(self.public_key) + '",\n'
        ret = ret + '  tags: "' + str(self.tags) + '",\n'
        ret = ret + '  members: "' + str(self.members) + '",\n'
        ret = ret + '  clock: "' + str(self.clock) + '",\n'
        ret = ret + '  listeners: "' + str(self.listeners) + '",\n'
        ret = ret + '}\n'
        return ret