def validate_ip(ip):
    a = ip.split('.')
    if len(a) != 4:
        return False
    for x in a:
        if not x.isdigit():
            return False
        i = int(x)
        if i < 0 or i > 255:
            return False
    return True


def validate_digit(port, start, stop):
    if port.isdigit():
        if start <= int(port) <= stop:
            return True
        else:
            return False
    else:
        return False


def validate_in_enum(enum, input_data):
    if input_data in enum:
        return True
    else:
        return False