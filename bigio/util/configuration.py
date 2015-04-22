__author__ = 'atrimble'

PROTOCOL_PROPERTY = "io.bigio.protocol"
DEFAULT_PROTOCOL = "tcp"

ADDRESS_PROPERTY = "io.bigio.address"
DEFAULT_ADDRESS = "127.0.0.1"

GOSSIP_PORT_PROPERTY = "io.bigio.port.gossip"
DATA_PORT_PROPERTY = "io.bigio.port.data"

SSL_PROPERTY = "io.bigio.ssl"
DEFAULT_SSL = False

SSL_SELFSIGNED_PROPERTY = "io.bigio.ssl.selfSigned"
DEFAULT_SELFSIGNED = True

SSL_CERTCHAINFILE_PROPERTY = "io.bigio.ssl.certChainFile"
DEFAULT_CERTCHAINFILE = "conf/certChain.pem"

SSL_KEYFILE_PROPERTY = "io.bigio.ssl.keyFile"
DEFAULT_KEYFILE = "conf/keyfile.pem"

SSL_KEYPASSWORD_PROPERTY = "io.bigio.ssl.keyPassword"

ENCRYPTION_PROPERTY = "io.bigio.encryption"
DEFAULT_ENCRYPTION = False

MULTICAST_GROUP_PROPERTY = "io.bigio.multicast.group"
DEFAULT_MULTICAST_GROUP = "239.0.0.1"

MULTICAST_PORT_PROPERTY = "io.bigio.multicast.port"
DEFAULT_MULTICAST_PORT = 8989

GOSSIP_INTERVAL_PROPERTY = "io.bigio.gossip.interval"
DEFAULT_GOSSIP_INTERVAL = "250"

CLEANUP_INTERVAL_PROPERTY = "io.bigio.gossip.cleanup"
DEFAULT_CLEANUP_INTERVAL = "10000"