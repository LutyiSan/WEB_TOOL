from flask import render_template, request
from validator import *
from operation import *


class Router:

    def __init__(self):
        self.ret_data = 'Sorry, Function in development!'
        self.request = request
        self.operate_dict = dict()

    def home(self):

        return render_template('home.html', response='')

    def __ip_port(self):
        ip = self.request.args.get("host-ip")

        if ip is not None:
            if validate_ip(ip):
                self.operate_dict['host_ip'] = ip
            else:
                self.operate_dict['host_ip'] = None
        else:
            self.operate_dict['host_ip'] = None
        dip = self.request.args.get("device-ip")
        if dip is not None:
            if validate_ip(dip):
                self.operate_dict['device_ip'] = dip
            else:
                self.operate_dict['device_ip'] = None
        else:
            self.operate_dict['device_ip'] = None
        port = self.request.args.get("port")
        if port is not None:
            if validate_digit(port, 1, 65535):
                self.operate_dict['port'] = port
            else:
                self.operate_dict['port'] = None
        else:
            self.operate_dict['port'] = None

    def __id(self):
        instance = self.request.args.get("instance")
        if instance is not None:
            if validate_digit(instance, 0, 65535):
                self.operate_dict['obj_id'] = instance
            else:
                self.operate_dict['obj_id'] = None
        else:
            self.operate_dict['obj_id'] = None

    def __obj_type(self):
        self.operate_dict['obj_type'] = self.request.args.get("object-type")

    def __quantity(self):
        quantity = self.request.args.get("quantity")
        if quantity is not None:
            if validate_digit(quantity, 1, 125):
                self.operate_dict['quantity'] = quantity
            else:
                self.operate_dict['quantity'] = None
        else:
            self.operate_dict['quantity'] = None

    def route_controller(self, route):
        if route == '/protocol/modbus/read':
            valid = True
            self.__ip_port()
            self.__id()
            self.__obj_type()
            self.__quantity()
            for i in self.operate_dict:
                if i != 'host_ip':
                    if self.operate_dict[i] is None:
                        valid = False
            if not valid:
                return render_template('home.html', response='Wrong input DATA!!!')
            else:
                self.ret_data = modbus_read(self.operate_dict)
                return render_template('home.html', response=self.ret_data)
        elif route == '/protocol/bacnet/whois':
            self.__ip_port()
            return render_template('home.html', response=self.ret_data)
        elif route == '/protocol/bacnet/gol':
            valid = True
            self.__ip_port()
            self.__id()
            for i in self.operate_dict:
                if self.operate_dict[i] is None:
                    valid = False
            if not valid:
                return render_template('home.html', response='Wrong input DATA!!!')
            else:
                self.ret_data = bacnet_obj_list(self.operate_dict)
                length = len(self.ret_data['OBJECT_ID'])
                signal = self.ret_data
                return render_template('f.html', len=length, signals=signal)
        elif route == '/protocol/bacnet/read':
            valid = True
            self.__ip_port()
            self.__obj_type()
            self.__id()
            for i in self.operate_dict:
                if self.operate_dict[i] is None:
                    valid = False
            if not valid:
                return render_template('home.html', response='Wrong input DATA!!!')
            else:
                self.ret_data = bacnet_read(self.operate_dict)
                return render_template('home.html', response=self.ret_data)
