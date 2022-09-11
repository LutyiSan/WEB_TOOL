from BAC0.scripts.Lite import Lite
from colorama import Fore
from validator import *


def sign_sf(sf):
    if sf is not None and len(sf) == 4:
        if sf[0] and sf[0] != 'Null':
            sf[0] = 'in-alarm'
        if sf[1] and sf[1] != 'Null':
            sf[1] = 'fault'
        if sf[2] and sf[2] != 'Null':
            sf[2] = 'overridden'
        if sf[3] and sf[3] != 'Null':
            sf[3] = 'is-not-service'
        return sf
    else:
        return [None, None, None, None]


class BACnet:
    def __init__(self, host_ip="localhost", netmask='24', listen_port=47808):
        self.single_point_list = []
        self.object_dict = {'OBJECT_TYPE': [], 'OBJECT_ID': [], 'OBJECT_NAME': []}
        self.i_am_dict = {'DEVICE_IP': [], 'DEVICE_ID': [], "DEVICE_NAME": [], 'VENDOR': []}
        self.my_interface = host_ip
        self.netmask = netmask
        self.listen_port = listen_port

    def create_client(self):
        try:
            self.bacnet_client = Lite(ip=self.my_interface, port=self.listen_port)
            print(Fore.LIGHTGREEN_EX + "BACnet Client READY")
            return True
        except Exception as e:
            print(Fore.LIGHTRED_EX + "FAIL create BACnet Client", e)
            return False

    def who_is(self):
        i_am_list = None
        name = None
        vendor = None
        try:
            i_am_list = self.bacnet_client.whois()
            print(i_am_list)
        except Exception as e:
            print(Fore.LIGHTRED_EX + "NO RESPONSE WHO-IS", e)
        if len(i_am_list) > 0:
            for i in i_am_list:
                if validate_ip(i[0]):
                    try:
                        name = self.bacnet_client.read(f'{i[0]}/{self.netmask} device {i[1]} objectName')
                    except:
                        print(f'No response NAME-request: {i[0]} | {i[1]}')
                    try:
                        vendor = self.bacnet_client.read(f'{i[0]}/{self.netmask} device {i[1]} vendorName')
                    except:
                        print(f'No response VENDOR-request: {i[0]} | {i[1]}')

                    self.i_am_dict['DEVICE_IP'].append(i[0])
                    self.i_am_dict['DEVICE_ID'].append(i[1])
                    if isinstance(name, (str, list)) and len(name) > 0:
                        self.i_am_dict['DEVICE_NAME'].append(name)
                    else:
                        name = "unknown"
                        self.i_am_dict['DEVICE_NAME'].append('unknown')
                    if isinstance(name, (str, list)) and len(name) > 0:
                        self.i_am_dict['VENDOR'].append(vendor)
                    else:
                        vendor = "unknown"
                        self.i_am_dict['VENDOR'].append('unknown')
                    print(Fore.LIGHTGREEN_EX + f'ip: {i[0]} | id: {i[1]} | name: {name} | vendor: {vendor}')

        self.bacnet_client.disconnect()

        return self.i_am_dict

    def read_single(self, device_ip, object_type, object_id):
        object_types = {"ai": 'analogInput', 'ao': 'analogOutput', 'av': 'analogValue', 'bi': 'binaryInput',
                        'bo': 'binaryOutput', 'bv': 'binaryValue', 'msi': 'multiStateInput', 'mso': 'multiStateOutput',
                        'msv': 'multiStateValue'}
        obj_type = object_types[f'{object_type}']
        try:
            pv = self.bacnet_client.read(f'{device_ip}/{self.netmask} {obj_type} {object_id} presentValue')
            if isinstance(pv, (str, int, float)):
                self.single_point_list.append(pv)
                sf = self.bacnet_client.read(f'{device_ip}/{self.netmask} {obj_type} {object_id} statusFlags')
                if isinstance(sf, list) and len(sf) == 4:
                    self.single_point_list.append(sf)
                else:
                    self.single_point_list.append('unknown')
                try:
                    rl = self.bacnet_client.read(f'{device_ip}/{self.netmask} {obj_type} {object_id} reliability')
                    if isinstance(sf, (list, str)) and len(sf) > 0:
                        self.single_point_list.append(rl)
                    else:
                        self.single_point_list.append('unknown')
                except Exception as e:
                    self.single_point_list.append('unknown')
                    print(e)
            else:
                self.single_point_list.append('unknown')
            print(Fore.LIGHTGREEN_EX + f'{obj_type} | {object_id} | {self.single_point_list[0]} | '
                                       f'{self.single_point_list[1]} | {self.single_point_list[2]}')
            result = f'{obj_type} | {object_id} | {self.single_point_list[0]} | {self.single_point_list[1]} | {self.single_point_list[2]}'

        except Exception as e:
            print(Fore.LIGHTRED_EX + "Can't read property", e)
            return str(e)
        sf = sign_sf(self.single_point_list[1])
        return f'{obj_type} - {object_id} | present-value={self.single_point_list[0]} status-flags={sf} reliability={self.single_point_list[2]}'

    def get_object_list(self, device_ip, device_id):

        try:
            object_list = self.bacnet_client.read(
                f'{device_ip}/{self.netmask} device {device_id} objectList')

            objects_len = len(object_list)
            if objects_len > 0:
                for i in object_list:
                    self.name = self.bacnet_client.read(
                        f'{device_ip}/{self.netmask} {i[0]} {i[1]} objectName')

                    self.object_dict['OBJECT_TYPE'].append(i[0])
                    self.object_dict['OBJECT_ID'].append(i[1])
                    if isinstance(self.name, (str, list)) and len(self.name) > 0:
                        self.object_dict['OBJECT_NAME'].append(self.name)
                    else:
                        self.object_dict['OBJECT_NAME'].append('unknown')
            sent_data = dict.fromkeys(self.object_dict['OBJECT_NAME'])
            idx = -1
            while idx < (len(self.object_dict['OBJECT_NAME']) - 1):
                idx += 1
                sent_data[self.object_dict['OBJECT_NAME'][
                    idx]] = f"{self.object_dict['OBJECT_TYPE'][idx]} {self.object_dict['OBJECT_ID'][idx]}"
            return sent_data
        except Exception as e:
            print(Fore.LIGHTRED_EX + "Can't get object-list", e)
            return False


    def disconnect(self):
        self.bacnet_client.disconnect()
        pass

