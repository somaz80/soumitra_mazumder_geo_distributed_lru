from flask import Flask, request, jsonify
import requests
import asyncio
from asyncio import coroutines
import simplejson
from flask import Response, Request
import collections
import os
import glob
import json

cache = collections.OrderedDict()
servers = []
back_up_timer_server = []

app = Flask('Server_1')


def set_up(app):
    servers.append(['127.0.0.1', 5452])
    servers.append(['127.0.0.1', 5453])
    back_up_timer_server.append(['127.0.0.1', 5456])


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
    reconcile_with_other_servers(item_key, item_value)
    return jsonify({item_key: item_value})


# def invoke_cache_update():
def reconcile_with_other_servers(item_key, item_value):
    input_dict = {'item_key': item_key, 'item_value': item_value}
    headers = {'Content-type': 'application/json', 'relay-update': False}
    r = requests.post("http://127.0.0.1:5451/setCacheItem", headers=headers,
                      json=input_dict)
    return r.status_code


@app.route('/updateCacheItem', methods=['PUT'])
@asyncio.coroutine
def update_cache_item():
    content = request.json
    item_key = content['item_key']
    item_value = content['item_value']
    cache[item_key] = item_value
    return jsonify({item_key: item_value})


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5451, debug=True)
