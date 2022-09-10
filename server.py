from flask import Flask
from route_func import *

app = Flask(__name__)
router = Router()


@app.route('/')
def enter():
    return router.home()


@app.route('/protocol/modbus/read', methods=['GET'])
def mb_read():
    return router.route_controller('/protocol/modbus/read')


@app.route('/protocol/bacnet/whois', methods=['GET'])
def bc_who_is():
    return router.route_controller('/protocol/bacnet/whois')


@app.route('/protocol/bacnet/gol', methods=['GET'])
def bc_gol():
    return router.route_controller('/protocol/bacnet/gol')


@app.route('/protocol/bacnet/read', methods=['GET'])
def bc_read():
    return router.route_controller('/protocol/bacnet/read')


app.run(host='127.0.0.1', port=90)
