from flask import render_template, request
from validator import *
from operation import *


class Router:

    def __init__(self):
        self.ret_data = 'Sorry, Function in development!'
        self.request = request
        self.operate_dict = dict()

    def __ip_port(self):
        ip = self.request.args.get("host-ip")
        self.operate_dict['host_ip'] = ip
        dip = self.request.args.get("device-ip")
        self.operate_dict['device_ip'] = dip
        port = self.request.args.get("port")
        self.operate_dict['port'] = port

    def __id(self):
        instance = self.request.args.get("instance")
        self.operate_dict['obj_id'] = instance

    def __obj_type(self):
        self.operate_dict['obj_type'] = self.request.args.get("object-type")

    def __quantity(self):
        quantity = self.request.args.get("quantity")
        self.operate_dict['quantity'] = quantity

    def route_controller(self, route):
        if route == '/protocol/modbus/read':
            self.__ip_port()
            self.__id()
            self.__obj_type()
            self.__quantity()
            self.ret_data = modbus_read(self.operate_dict)
            return self.ret_data
        elif route == '/protocol/bacnet/whois':
            self.__ip_port()
            return render_template('home.html', response=self.ret_data)
        elif route == '/protocol/bacnet/gol':
            self.__ip_port()
            self.__id()
            self.ret_data = bacnet_obj_list(self.operate_dict)
            return self.ret_data
        elif route == '/protocol/bacnet/read':
            self.__ip_port()
            self.__obj_type()
            self.__id()
            self.ret_data = bacnet_read(self.operate_dict)
            return self.ret_data
