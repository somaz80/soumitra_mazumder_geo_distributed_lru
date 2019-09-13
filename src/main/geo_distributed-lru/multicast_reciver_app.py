import json
import socket
import struct
import sys

import requests

from common_constants import CommonConstants


class MulticastReceiver:

    def __init__(self, multicast_group_ip, multicast_server_port, cache_server_port):
        self.multicast_group = multicast_group_ip
        self.server_address = ('', multicast_server_port)
        self.cache_server_port = cache_server_port

    # retuns back a socket for interaction on a multicast host
    def get_reciver_socket(self):
        # Create the socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        # Bind to the server address
        sock.bind(self.server_address)

        group = socket.inet_aton(self.multicast_group)
        mreq = struct.pack('4sL', group, socket.INADDR_ANY)
        sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
        return sock

    '''
    this program keeps on running on background as receiver to listen to incoming update and forward
    '''

    def listen_incoming_request_send_update_to_cache(self, sock):
        # Receive/respond loop
        while True:
            print(sys.stderr, 'waiting to receive message')
            data, address = sock.recvfrom(CommonConstants.RECEIVER_SOCKET_BUFFER_SIZE)

            print(sys.stderr, 'received %s bytes from %s' % (len(data), address))
            print(sys.stderr, data)
            headers = {'Content-type': 'application/json'}
            """
            for the time being for testing using 127 IP. normally it should work with self.host_ip or hostname as well
            TODO: we have to check that if the receiver is running in the same box where the update of the
            cache has happened at first, if so then we might not want to call the update again on the same cache
            due to machine and  environment restriction i can not perform this task.
            """
            response = requests.put(f'http://localhost:{self.cache_server_port}/updateCacheItem',
                                    json=json.loads(data),
                                    headers=headers)
            print(sys.stderr, 'sending acknowledgement to', address)
            sock.sendto('ack'.encode(), address)

            print('Receiver program failed to execute update on the server')
            """
            TODO: if update results in error then we might have to queue the request in the queue and  then
            try to ping the server program for availability and  once it is available we might want to execute
            requests. For the time being just sending back the acknowledgement
            """


if __name__ == '__main__':
    rec = MulticastReceiver(CommonConstants.MULTICAST_GROUP_IP, CommonConstants.MULTICAST_PORT_VALUE,
                            CommonConstants.SERVER_TWO_PORT)
    sock = rec.get_reciver_socket()
    rec.listen_incoming_request_send_update_to_cache(sock)
