from flask import Flask, render_template
from route_func import *
from server_class import Reference, Methods

app = Flask(__name__)
router = Router()
url = Reference()
meth = Methods


@app.route(url.home)
def enter():
    return render_template('home.html')


@app.route(url.mb_read, methods=[meth.get])
def read_registers():
    return router.route_controller(url.mb_read)


@app.route(url.obj_list, methods=[meth.get])
def get_obj_list():
    return router.route_controller(url.obj_list)


@app.route(url.bc_read, methods=[meth.get])
def read_property():
    return router.route_controller(url.bc_read)


@app.route(url.who_is, methods=[meth.get])
def bc_whois():
    return router.route_controller(url.who_is)


app.run(host='127.0.0.1', port=90, debug=True)
