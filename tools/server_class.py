class Reference:
    home = '/'
    section = 'protocol/'
    bacnet = 'bacnet/'
    modbus = 'modbus/'
    read = 'read'
    get_object_list = 'gol'
    whois = 'whois'
    mb_read = home + section + modbus + read
    obj_list = home + section + bacnet + get_object_list
    bc_read = home + section + bacnet + read
    who_is = home + section + bacnet + whois


class Methods:
    get = 'GET'
    post = 'POST'
