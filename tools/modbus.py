from pymodbus.client.sync import ModbusTcpClient as ModbusClient
from pymodbus.pdu import ExceptionResponse
from loguru import logger
from colorama import Fore, init

UNIT = 0x1


class TCPClient:
    def __init__(self, ip_address, tcp_port):
        init(autoreset=False)

        self.tester = ModbusClient(str(ip_address), int(tcp_port))
        self.tester.timeout = 3.0
        self.tester.debug = True

    def connect(self):
        try:
            self.tester.connect()
            print("Modbus READY connected")
            return True
        except Exception as e:
            print("FAIL connecting", e)

    def read_hr(self, reg_address, quantity):
        try:
            result = self.tester.read_holding_registers(reg_address, quantity, unit=UNIT)
            if isinstance(result, ExceptionResponse):
                return False
            else:
                if result.registers:
                    if isinstance(result.registers, list):
                        return result.registers
                    else:
                        return False
                else:
                     return False
        except Exception as e:
            logger.exception(Fore.LIGHTRED_EX + "FAIL Read registers", e)
            return False

    def read_ir(self, reg_address, quantity):
        try:
            result = self.tester.read_input_registers(reg_address, quantity, unit=UNIT)
            if isinstance(result, ExceptionResponse):
                return False
            else:
                if result.registers:
                    if isinstance(result.registers, list):
                        return result.registers
                    else:
                        return False
                else:
                     return False
        except Exception as e:
            logger.exception(Fore.LIGHTRED_EX + "FAIL Read registers", e)
            return False

    # @func_set_timeout(5)
    def read_coils(self, reg_address, quantity):
        try:
            result = self.tester.read_coils(reg_address, quantity, unit=UNIT)
            print(result.bits)
            if isinstance(result.bits, list):
                return result.bits
            else:
                return False
        except Exception as e:
            print(Fore.LIGHTRED_EX + "FAIL Read registers", e)
            return False

    #  @func_set_timeout(5)
    def read_di(self, reg_address, quantity):
        try:
            result = self.tester.read_discrete_inputs(reg_address, quantity, unit=UNIT)
            print(result)
            if isinstance(result.bits, list):
                return result.bits
            else:
                return False
        except Exception as e:
            print(Fore.LIGHTRED_EX + "FAIL Read registers", e)
            return False

    def read(self, reg_address, quantity, reg_type):
        if self.connect():
            result = None
            if reg_type == 'hr':
                try:
                    result = self.read_hr(int(reg_address), int(quantity))
                except Exception as e:
                    print(Fore.LIGHTRED_EX + "READ TIMEOUT", e)
            elif reg_type == 'ir':
                try:
                    result = self.read_ir(int(reg_address), int(quantity))
                except Exception as e:
                    print(Fore.LIGHTRED_EX + "READ TIMEOUT", e)
            elif reg_type == 'di':
                try:
                    result = self.read_di(int(reg_address), int(quantity))
                except Exception as e:
                    print(Fore.LIGHTRED_EX + "READ TIMEOUT", e)
            elif reg_type == 'co':
                try:
                    result = self.read_coils(int(reg_address), int(quantity))
                except Exception as e:
                    print(Fore.LIGHTRED_EX + "READ TIMEOUT", e)
            self.disconnect()
            return result

    def disconnect(self):
        try:
            self.tester.close()
            print(Fore.LIGHTGREEN_EX + "Connection closed")
        except Exception as e:
            print(Fore.LIGHTRED_EX + "FAIL close connection", e)
