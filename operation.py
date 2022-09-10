from modbus import TCPClient
from bacnet import BACnet


def modbus_read(operate_dict):
    client = TCPClient(operate_dict['device_ip'], operate_dict['port'])
    client.connect()

    return client.read(operate_dict['obj_id'], operate_dict['quantity'], operate_dict['obj_type'])


def bacnet_read(operate_dict):
    client = BACnet(host_ip=operate_dict['host_ip'], listen_port=operate_dict['port'])
    if client.create_client():
        result = client.read_single(operate_dict['device_ip'], operate_dict['obj_type'], int(operate_dict['obj_id']))
        client.disconnect()
        return result


def bacnet_obj_list(operate_dict):
    client = BACnet(host_ip=operate_dict['host_ip'], listen_port=operate_dict['port'])
    if client.create_client():
        result = client.get_object_list(operate_dict['device_ip'], int(operate_dict['obj_id']))
        client.disconnect()
        return result
