import collections
import asyncio
from flask import Flask, request, jsonify
import socket

cache = collections.OrderedDict()
servers = []
back_up_timer_server = []

app = Flask('Server_1')


def set_up(app):
    servers.append(['soumitras-mbp.c4p-in.ibmmobiledemo.com', 5455])
    #servers.append(['127.0.0.1', 5453])
    #servers.append(['127.0.0.1', 5451])
    back_up_timer_server.append(['127.0.0.1', 5456])


set_up(app)


@app.route('/heartbeat', methods=['GET'])
def get_heartbeat():
    return jsonify({'heartbeat': 'success'})


# return a socket server socket
def get_server_socket():
    s = None
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print('Socket successfully created')
    except socket.error as err:
        print(f'socket creation failed with error {err}')
    return s


# @app.route('/updateCaches', methods=['POST'])
# def update_caches():
#     server_socket = get_server_socket()
#     for server in servers:
#         server_socket.connect((server[0], server[1]))
#         print(server_socket.recv(1024).decode())
#         server_socket.close()


@app.route('/updateCaches', methods=['POST'])
def update_caches():




if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5454, debug=True)
