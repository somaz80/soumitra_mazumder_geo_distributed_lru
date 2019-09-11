import json
import socket
import struct

from flask import Flask, request, jsonify

from common_constants import CommonConstants
from distributed_lru.lru_cache import LRUCache

cache = LRUCache(CommonConstants.MAXIMUM_CACHE_ELEMENT_CAPACITY, CommonConstants.CACHE_EXPIRY_IN_SECONDS)

app = Flask('LRU_CACHE_SERVER_ONE')


# def set_up(app):


# set_up(app)


@app.route('/heartbeat', methods=['GET'])
def get_heartbeat():
    return jsonify({'heartbeat': 'success'})


@app.route('/getCacheItem', methods=['GET'])
def get_cache_item():
    item_key = request.args['item_key']
    key, value, expires_at = cache.get_element_from_cache(item_key)
    return jsonify({'item_key': key, 'value': value, 'expires_at': expires_at})


@app.route('/setCacheItem', methods=['POST'])
def set_cache_item():
    content = request.json
    item_key = content['item_key']
    item_value = content['item_value']
    expires_at = content['expires_at']
    cache.set_element_in_cache(item_key, item_value, expires_at)
    multicast_sender({'key': item_key, 'value': item_value, 'expires_at': expires_at, 'action': 'set'})
    return jsonify({item_key: item_value})


@app.route('/deleteCacheItem', methods=['DELETE'])
def delete_cache_item():
    item_key = request.args['item_key']
    flag_value = cache.delete_item_from_cache(item_key)
    multicast_sender({'key': item_key, 'action': 'delete'})
    return jsonify({item_key: flag_value})


# # def invoke_cache_update():
# def broadcast_update(item_key, item_value):
#     input_dict = {'item_key': item_key, 'item_value': item_value}
#     headers = {'Content-type': 'application/json', 'relay-update': False}
#     #server_string = f'http://{sync_server[0][0]}:{sync_server[0][1]}/updateCaches'
#     r = requests.post(server_string, headers=headers,
#                       json=input_dict)
#     return r.status_code

'''
    This function is responsible for sending out json message to the multicast group members
'''


def multicast_sender(data):

    multicast_group = (CommonConstants.MULTICAST_GROUP_IP, CommonConstants.MULTICAST_PORT_VALUE)

    # Create the datagram socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Set a timeout so the socket does not block indefinitely when trying
    # to receive data.
    sock.settimeout(CommonConstants.SENDER_SOCKET_TIME_OUT)

    # Set the time-to-live for messages to 1 so they do not go past the
    # local network segment.
    ttl = struct.pack('b', CommonConstants.TIME_TO_LIVE_FOR_MESSAGE)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl)

    try:

        # Send data to the multicast group
        print(f'sending{data}')
        sent = sock.sendto(json.dumps(data).encode(), multicast_group)

        # Look for responses from all recipients
        while True:
            print('waiting to receive')
            try:
                data, server = sock.recvfrom(CommonConstants.SENDER_SOCKET_BUFFER_SIZE)
            except socket.timeout:
                print('timed out, no more responses')
                break
            else:
                print('received ---', data, server)

    finally:
        print('closing socket')
        sock.close()


@app.route('/updateCacheItem', methods=['PUT'])
def update_cache_item():
    content = request.json
    item_key = content['key']
    item_value = content['value']
    item_action = content['action']
    expires_at = content['expires_at']
    if item_action is 'delete':
        cache.delete_item_from_cache(item_key)
    else:
        cache.set_element_in_cache(item_key, item_value, expires_at)
    return jsonify({item_key: item_value})


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5454, debug=True)
