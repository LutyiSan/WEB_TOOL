from flask import Flask
from route_func import *

app = Flask(__name__)
router = Router()


@app.route('/')
def enter():
    return render_template('home.html')


@app.route('/protocol/modbus/read', methods=['GET'])
def read_registers():
    return router.route_controller('/protocol/modbus/read')


@app.route('/protocol/bacnet/whois', methods=['GET'])
def who_is():
    return router.route_controller('/protocol/bacnet/whois')


@app.route('/protocol/bacnet/gol', methods=['GET'])
def get_obj_list():
    return router.route_controller('/protocol/bacnet/gol')


@app.route('/protocol/bacnet/read', methods=['GET'])
def read_property():
    return router.route_controller('/protocol/bacnet/read')


app.run(host='127.0.0.1', port=90)
