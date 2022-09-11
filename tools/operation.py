from tools.modbus import TCPClient
from tools.bacnet import BACnet


def modbus_read(operate_dict):
    res_dict = dict()
    client = TCPClient(operate_dict['device_ip'], operate_dict['port'])
    client.connect()
    res = client.read(operate_dict['obj_id'], operate_dict['quantity'], operate_dict['obj_type'])
    if res:
        for i in range(0, len(res)):
            res_dict[f'address-{int(operate_dict["obj_id"]) + i}'] = res[i]
    else:
        for i in range(0, int(operate_dict['quantity'])):
            res_dict[f'address-{int(operate_dict["obj_id"]) + i}'] = "  FAIL read"
    return res_dict


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
        if result:
            return result
        else:
            return {'OBJECT_TYPE': [], 'OBJECT_ID': [], 'OBJECT_NAME': []}
