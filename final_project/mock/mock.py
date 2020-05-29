import threading

from flask import Flask, abort, request

app = Flask(__name__)
users = {}


def run_mock(host, port):
    server = threading.Thread(target=app.run, kwargs={'host': host, 'port': port})
    server.start()
    return server


def shutdown_mock():
    terminate_func = request.environ.get('werkzeug.server.shutdown')
    if terminate_func:
        terminate_func()


@app.route('/vk_id/add')
def add_user_by_id():
    user_id = request.args.get("username")
    vk_id = request.args.get("vk_id")
    users.update({user_id: vk_id})
    return {'vk_id': vk_id}, 200, {'ContentType': 'application/json'}


@app.route('/vk_id/<username>', methods=["GET"])
def get_user_by_id(username):
    vk_id = users.get(username, None)
    if vk_id:
        return {'vk_id': vk_id}, 200, {'ContentType':'application/json'}
    else:
        return dict(), 404, {'ContentType':'application/json'}


@app.route('/vk_id/delete', methods=["POST"])
def delete_user_by_id():
    user_id = request.args.get("username")
    if users.get(user_id, None):
        user = users.pop(user_id)
        return {user_id: user}, 200, {'ContentType':'application/json'}
    else:
        return dict(), 404, {'ContentType':'application/json'}


@app.route('/shutdown')
def shutdown():
    shutdown_mock()


if __name__ == '__main__':
    host = '0.0.0.0'
    port = 5000
    server = run_mock(host, port)
