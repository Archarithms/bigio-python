__author__ = 'atrimble'

import random
import socket
import bigio.parameters as parameters
import netifaces
import logging

logger = logging.getLogger(__name__)

START_PORT = 32768
END_PORT = 65536
NUM_CANDIDATES = END_PORT - START_PORT + 1
NETWORK_INTERFACE_PROPERTY = "io.bigio.network"

ip = None


def get_free_port():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.bind(("localhost", 0))
        port = s.getsockname()[1]
    finally:
        s.close()

    return port


def get_ip():
    print(netifaces.interfaces())
    print(socket.gethostbyname(socket.gethostname()))
    global ip

    if ip:
        return ip

    ip = socket.gethostbyname(socket.gethostname())
    return ip

    nic = parameters.get_property(NETWORK_INTERFACE_PROPERTY)
    # if not nic:
    #     interfaces = os.networkInterfaces()
    #     os = parameters.current_os()
    #
    #     switch(parameters.getInstance().currentOS()):
    #         case OperatingSystem.WIN_64:
    #         case OperatingSystem.WIN_32:
    #             match = "Loopback";
    #             break;
    #         case OperatingSystem.LINUX_64:
    #         case OperatingSystem.LINUX_32:
    #             match = "lo";
    #             break;
    #         case OperatingSystem.MAC_64:
    #         case OperatingSystem.MAC_32:
    #             match = "lo0";
    #             break;
    #         default:
    #             logger.error("Cannot determine operating system. Cluster cannot form.");


    return