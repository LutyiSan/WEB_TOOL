from pymodbus.client.sync import ModbusTcpClient as ModbusClient
from loguru import logger
from tools.validator import validate_ip, validate_digit


class ModbusTCPClient:
    unit = 0x1
    mb_logger = logger
    fault = []
    min_address = 0
    max_address = 65535
    min_quantity = 1
    max_quantity = 124

    def connection(self, ip_address: str, tcp_port=502, timeout=3.0) -> bool:
        if not validate_ip(ip_address):
            self.mb_logger.error('IP-address incorrect!')
            return False
        if not validate_digit(tcp_port, 1, 65535):
            self.mb_logger.error('Port number incorrect!')
            return False
        if not validate_digit(timeout, 1, 10):
            self.mb_logger.error('Timeout value incorrect!')
            return False
        self.client = ModbusClient(ip_address, port=tcp_port, timeout=timeout)
        try:
            self.client.connect()
            return True
        except Exception as e:
            self.mb_logger.exception(e)

    def read_registers(self, reg_number: int, quantity: int, reg_type: str) -> list:
        if not validate_digit(reg_number, self.min_address, self.max_address):
            self.mb_logger.error('Registers address incorrect!')
            return self.__append_fault(quantity)
        if not validate_digit(quantity, self.min_quantity, self.max_quantity):
            self.mb_logger.error('Quantity value incorrect!')
            return self.__append_fault(quantity)
        try:
            if reg_type == 'hr':
                result = self.client.read_holding_registers(reg_number, quantity, unit=self.unit)
            else:
                result = self.client.read_input_registers(reg_number, quantity, unit=self.unit)
            if isinstance(result.registers, list) and len(result.registers) == quantity:
                return result.registers
            else:
                return self.__append_fault(quantity)
        except Exception as e:
            self.mb_logger.exception("Fail read registers", e)
            return self.__append_fault(quantity)

    def read_bits(self, reg_number: int, quantity: int, reg_type: str) -> list:
        bits = []
        if not validate_digit(reg_number, self.min_address, self.max_address):
            self.mb_logger.error('Registers address incorrect!')
            return self.__append_fault(quantity)
        if not validate_digit(quantity, self.min_quantity, self.max_quantity):
            self.mb_logger.error('Quantity value incorrect!')
            return self.__append_fault(quantity)
        try:
            if reg_type == 'coils':
                result = self.client.read_coils(reg_number, quantity, unit=self.unit)
            else:
                result = self.client.read_discrete_inputs(reg_number, quantity, unit=self.unit)
            print(result)
            if isinstance(result.bits, list) and len(result.bits) >= quantity:
                for bit in range(0, quantity):
                    bits.append(result.bits[bit])
                return bits
            else:
                return self.__append_fault(quantity)
        except Exception as e:
            self.mb_logger.exception("Fail read registers", e)
            return self.__append_fault(quantity)

    def disconnect(self) -> None:
        try:
            self.client.close()
            logger.debug("Connection closed")
        except Exception as e:
            logger.exception("Can't close connection", e)

    def __append_fault(self, count: int) -> list:
        for _ in range(0, count):
            self.fault.append(None)
        return self.fault
