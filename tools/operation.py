from tools.modbus_driver import ModbusTCPClient
from tools.bacnet_driver import BACnetClient
from tools.converter import Convertor


def modbus_read(operate_dict):
    res_dict = dict()
    ret_string = ''
    if '16' in operate_dict['value-type']:
        operate_dict['quantity'] = int(operate_dict['quantity'])
    elif '32' in operate_dict['value-type']:
        operate_dict['quantity'] = int(operate_dict['quantity']) * 2
    elif '64' in operate_dict['value-type']:
        operate_dict['quantity'] = int(operate_dict['quantity']) * 4
    client = ModbusTCPClient()
    if client.connection(operate_dict['device_ip'], int(operate_dict['port'])):
        if operate_dict['obj_type'] in ['hr', 'ir']:
            res = client.read_registers(int(operate_dict['obj_id']), operate_dict['quantity'],
                                        operate_dict['obj_type'])
            if None in res:
                return 'Fail read registers!, '
            else:
                convert_data = mb_convert(operate_dict, res)
                for i in range(0, len(convert_data['values'])):
                    ret_string += f'address: {convert_data["address"][i]}  value: {convert_data["values"][i]}  |,'
                return ret_string
        elif operate_dict['obj_type'] in ['di', 'co']:
            res = client.read_bits(int(operate_dict['obj_id']), int(operate_dict['quantity']), operate_dict['obj_type'])
            if None in res:
                return 'Fail read registers!, '
            else:
                for i in range(0, len(res)):
                    res_dict[f'address-{int(operate_dict["obj_id"]) + i}'] = res[i]
            return res_dict
    else:
        return res_dict


def bacnet_read(operate_dict):
    operate_dict['port'] = int(operate_dict['port'])
    operate_dict['obj_id'] = int(operate_dict['obj_id'])
    client = BACnetClient()
    if client.create(ip_address=operate_dict['host_ip'], port=operate_dict['port']):
        result = client.read_single(operate_dict)
        client.disconnect()
        if result['present-value'] == [None] and result['status-flags'] == [None, None, None, None]:
            return 'FAIL read property!, Maybe property is absent in device!'
        if result:
            return dict_to_string(result)
        else:
            return 'FAIL read property!, Maybe property is absent in device!'
    else:
        return 'FAIL read property!, Check host-ip and BACnet-Port!'


def bacnet_obj_list(operate_dict):
    operate_dict['port'] = int(operate_dict['port'])
    operate_dict['obj_id'] = int(operate_dict['obj_id'])
    out = ''
    client = BACnetClient()
    if client.create(ip_address=operate_dict['host_ip'], port=operate_dict['port']):
        result = client.get_object_list(operate_dict)
        client.disconnect()
        if result:
            idx = -1
            while idx < (len(result['type']) - 1):
                idx += 1
                out += f'name: {result["name"][idx]} type: {result["type"][idx]} id: {result["id"][idx]},'
            return out
        else:
            return 'Fail get object list!, No answer from device!'
    else:
        return 'Fail get object-list!, Check host-ip and BACnet-Port!'


def bacnet_whois(operate_dict):
    operate_dict['port'] = int(operate_dict['port'])
    client = BACnetClient()
    if client.create(ip_address=operate_dict['host_ip'], port=operate_dict['port']):
        result = client.who_is()
        client.disconnect()
        if result:
            return dict_to_string(result)
        else:
            return 'No response who-is!, No response from devices!'

    else:
        return 'No response who-is!, Check host-ip and BACnet-Port!'


def dict_to_string(data: dict) -> str or None:
    if not isinstance(data, dict):
        return None
    out_string = ''
    for key in data:
        out_string += f"{key}: {data[key]},"
    return out_string


def mb_convert(data: dict, values):
    ret_dict = {'address': [], 'values': []}
    data_type = data['value-type']
    idx = 0
    while idx < int(data['quantity']):
        ret_dict['address'].append(int(data['obj_id']) + idx)
        if '32' in data_type:
            ret_dict['values'].append(Convertor.converting_choice([values[idx], values[idx + 1]], data_type))
            idx += 2
        elif '64' in data_type:
            ret_dict['values'].append(Convertor.converting_choice([values[idx], values[idx + 1], values[idx + 2],
                                                                   values[idx + 2]], data_type))
            idx += 4
        else:
            ret_dict['values'].append(Convertor.converting_choice(values[idx], data_type))
            idx += 1
    return ret_dict
