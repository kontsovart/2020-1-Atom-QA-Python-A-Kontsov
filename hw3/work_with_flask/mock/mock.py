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


@app.route('/user')
def add_data():
    user_id = int(request.args.get("user_id"))
    first_name = request.args.get("first_name")
    last_name = request.args.get("last_name")
    users.update({user_id: [first_name, last_name]})


@app.route('/user/<user_id>', methods=["GET"])
def get_user_by_id(user_id: int):
    user = users.get(int(user_id), None)
    if user:
        return {user_id: user}, 200, {'ContentType':'application/json'}
    else:
        abort(404)


@app.route('/user/delete', methods=["POST"])
def delete_user_by_id():
    user_id = int(request.args.get("user_id"))
    if users.get(user_id, None):
        user = users.pop(user_id)
        return {user_id: user}, 200, {'ContentType':'application/json'}
    else:
        return 404


@app.route('/shutdown')
def shutdown():
    shutdown_mock()
