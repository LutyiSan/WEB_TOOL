from flask import request
from operation import *
from server_class import Reference

ref = Reference()


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

    def __value_type(self):
        data_type = self.request.args.get("value-type")
        print(data_type)
        self.operate_dict['value-type'] = data_type

    def route_controller(self, route):
        if route == ref.mb_read:
            self.__ip_port()
            self.__id()
            self.__obj_type()
            self.__quantity()
            self.__value_type()
            self.ret_data = modbus_read(self.operate_dict)
            return self.ret_data
        elif route == ref.obj_list:
            self.__ip_port()
            self.__id()
            self.ret_data = bacnet_obj_list(self.operate_dict)
            return self.ret_data
        elif route == ref.bc_read:
            self.__ip_port()
            self.__obj_type()
            self.__id()
            self.ret_data = bacnet_read(self.operate_dict)
            return self.ret_data
        elif route == ref.who_is:
            self.__ip_port()
            self.ret_data = bacnet_whois(self.operate_dict)
            return self.ret_data
