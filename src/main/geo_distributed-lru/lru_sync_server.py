import collections
import asyncio
from flask import Flask, request, jsonify

cache = collections.OrderedDict()
servers = []
back_up_timer_server = []

app = Flask('Server_1')


def set_up(app):
    servers.append(['127.0.0.1', 5452])
    servers.append(['127.0.0.1', 5453])
    servers.append(['127.0.0.1', 5451])
    back_up_timer_server.append(['127.0.0.1', 5456])


set_up(app)


@app.route('/heartbeat', methods=['GET'])
def get_heartbeat():
    return jsonify({'heartbeat': 'success'})


@app.route('/updateCaches', methods=['POST'])
def update_caches():
    for server in servers:
        url_heartbeat = f'http://{server[0]}:{server[1]}/heartbeat'
        url_update = f'http://{server[0]}:{server[1]}/update_cache_item'

    content = request.json
    item_key = content['item_key']
    item_value = content['item_value']
    cache[item_key] = item_value
    return jsonify({item_key: item_value})


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5454, debug=True)
