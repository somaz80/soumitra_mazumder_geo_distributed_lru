from flask import Flask, request, jsonify
import collections
import os
import glob
import json

UPLOAD_FOLDER = '.'
app = Flask(__name__, static_url_path='')

cache = collections.OrderedDict()


@app.route('/getCacheItem', methods=['GET'])
def get_cache_item():
    item_key = request.args['item_key']
    item_value = cache.pop(item_key)
    return jsonify({item_key: item_value})


@app.route('/setCacheItem', methods=['POST'])
def set_cache_item():
    content = request.json
    item_key = content['item_key']
    item_value = content['item_value']
    cache[item_key] = item_value
    return jsonify({item_key: item_value})


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5452, debug=True)
