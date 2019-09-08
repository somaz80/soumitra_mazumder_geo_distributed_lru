import socket
import struct
import sys
import requests
import json
multicast_group = '224.3.29.71'
server_address = ('', 10000)

# Create the socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bind to the server address
sock.bind(server_address)
group = socket.inet_aton(multicast_group)
mreq = struct.pack('4sL', group, socket.INADDR_ANY)
sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
# Receive/respond loop
while True:
    print(sys.stderr, 'waiting to receive message')
    data, address = sock.recvfrom(1024)

    print(sys.stderr, 'received %s bytes from %s' % (len(data), address))
    print(sys.stderr, data)
    headers = {'Content-type': 'application/json'}
    r = requests.put("http://127.0.0.1:5453/updateCacheItem", json=json.loads(data), headers=headers)
    print(sys.stderr, 'sending acknowledgement to', address)
    sock.sendto('ack'.encode(), address)
