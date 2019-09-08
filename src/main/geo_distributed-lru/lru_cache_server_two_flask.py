import collections

import requests
import socket
import struct
import json
import sys
import asyncio
from flask import Flask, request, jsonify

cache = {}
servers = []
back_up_timer_server = []
sync_server = []

app = Flask('Server_1')


def update_cache_items(message):
    cache = json.loads(message)
    print('cache loaded', cache)


def set_up(app):
    servers.append(['127.0.0.1', 5452])
    servers.append(['127.0.0.1', 5453])
    back_up_timer_server.append(['127.0.0.1', 5456])
    sync_server.append(['127.0.0.1', 5454])



set_up(app)


@app.route('/heartbeat', methods=['GET'])
def get_heartbeat():
    return jsonify({'heartbeat': 'success'})


@app.route('/getCacheItem', methods=['GET'])
def get_cache_item():
    item_key = request.args['item_key']
    item_value = cache.get(item_key)
    return jsonify({item_key: item_value})


@app.route('/setCacheItem', methods=['POST'])
def set_cache_item():
    content = request.json
    item_key = content['item_key']
    item_value = content['item_value']
    cache[item_key] = item_value
    multicast_sender()
    return jsonify({item_key: item_value})


# def invoke_cache_update():
def broadcast_update(item_key, item_value):
    input_dict = {'item_key': item_key, 'item_value': item_value}
    headers = {'Content-type': 'application/json', 'relay-update': False}
    server_string = f'http://{sync_server[0][0]}:{sync_server[0][1]}/updateCaches'
    r = requests.post(server_string, headers=headers,
                      json=input_dict)
    return r.status_code


def multicast_sender():
    multicast_group = ('224.3.29.71', 10000)

    # Create the datagram socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Set a timeout so the socket does not block indefinitely when trying
    # to receive data.
    sock.settimeout(0.2)

    # Set the time-to-live for messages to 1 so they do not go past the
    # local network segment.
    ttl = struct.pack('b', 1)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl)

    try:

        # Send data to the multicast group
        print(f'sending{cache}')
        sent = sock.sendto(json.dumps(cache).encode(), multicast_group)

        # Look for responses from all recipients
        while True:
            print('waiting to receive')
            try:
                data, server = sock.recvfrom(16)
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
    item_key = content['item_key']
    item_value = content['item_value']
    cache[item_key] = item_value
    return jsonify({item_key: item_value})


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5453, debug=True)
