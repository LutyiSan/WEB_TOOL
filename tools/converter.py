from pymodbus.constants import Endian
from pymodbus.payload import BinaryPayloadDecoder


class Convertor:

    @staticmethod
    def converting_choice(values, data_type):
        if data_type == 'int16':
            return Convertor.to_int16(values, inverse=False)
        elif data_type == 'int16r':
            return Convertor.to_int16(values, inverse=True)
        elif data_type == 'int32':
            return Convertor.to_int32(values, inverse=False)
        elif data_type == 'int32r':
            return Convertor.to_int32(values, inverse=True)
        elif data_type == 'int64':
            return Convertor.to_int64(values, inverse=False)
        elif data_type == 'int64r':
            return Convertor.to_int64(values, inverse=True)
        elif data_type == 'uint16':
            return Convertor.to_uint16(values, inverse=False)
        elif data_type == 'uint16r':
            return Convertor.to_uint16(values, inverse=True)
        elif data_type == 'uint32':
            return Convertor.to_uint32(values, inverse=False)
        elif data_type == 'uint32r':
            return Convertor.to_uint32(values, inverse=True)
        elif data_type == 'uint64':
            return Convertor.to_uint64(values, inverse=False)
        elif data_type == 'uint64r':
            return Convertor.to_uint64(values, inverse=True)
        elif data_type == 'float16':
            return Convertor.to_float16(values, inverse=False)
        elif data_type == 'float16r':
            return Convertor.to_float16(values, inverse=True)
        elif data_type == 'float32':
            return Convertor.to_float32(values, inverse=False)
        elif data_type == 'float32r':
            return Convertor.to_float32(values, inverse=True)
        elif data_type == 'float64':
            return Convertor.to_float64(values, inverse=False)
        elif data_type == 'float64r':
            return Convertor.to_float64(values, inverse=True)
        elif data_type == 'binary16':
            return Convertor.to_16bit_array(values)

    @staticmethod
    def to_bool(value: int) -> bool or None:
        if not isinstance(value, int):
            return None
        else:
            if value:
                return True
            else:
                return False

    @staticmethod
    def to_bit(value: int, bit: int or None) -> bool or None:
        if not isinstance(value, int):
            return None
        else:
            bv = Convertor.to_16bit_array(value)
            if bv is None:
                return None
            if int(bv[bit]) == 1:
                return True
            else:
                return False

    @staticmethod
    def to_16bit_array(value: int) -> str or None:
        if not isinstance(value, int):
            return None
        bin_value = bin(value)[2:]
        if len(bin_value) != 16:
            zero_array = ""
            count = 16 - len(bin_value)
            i = 0
            while i < count:
                i += 1
                zero_array += '0'
            zero_array += bin_value
            return zero_array
        else:
            return bin_value

    @staticmethod
    def to_uint16(value: int, inverse=False) -> int or None:
        if inverse:
            bo = Endian.Little
        else:
            bo = Endian.Big
        if isinstance(value, int):
            decoder = BinaryPayloadDecoder.fromRegisters([value], byteorder=bo, wordorder=Endian.Big)
            return decoder.decode_16bit_uint()
        else:
            return None

    @staticmethod
    def to_int16(value: int, inverse=False) -> int or None:
        if inverse:
            bo = Endian.Little
        else:
            bo = Endian.Big
        if isinstance(value, int):
            decoder = BinaryPayloadDecoder.fromRegisters([value], byteorder=bo, wordorder=Endian.Big)
            return decoder.decode_16bit_int()
        else:
            return None

    @staticmethod
    def to_int32(values: list[int], inverse=False) -> int or None:
        if inverse:
            wo = Endian.Little
        else:
            wo = Endian.Big
        if isinstance(values, list) and len(values) == 2:
            for i in values:
                if not isinstance(i, int):
                    return None
                else:
                    decoder = BinaryPayloadDecoder.fromRegisters(values, byteorder=Endian.Big, wordorder=wo)
                    return decoder.decode_32bit_int()
        else:
            return None

    @staticmethod
    def to_int64(values: list[int], inverse=False) -> int or None:
        if inverse:
            wo = Endian.Little
        else:
            wo = Endian.Big
        if isinstance(values, list) and len(values) == 4:
            for i in values:
                if not isinstance(i, int):
                    return None
                else:
                    decoder = BinaryPayloadDecoder.fromRegisters(values, byteorder=Endian.Big, wordorder=wo)
                    return decoder.decode_64bit_int()
        else:
            return None

    @staticmethod
    def to_uint32(values: list[int], inverse=False) -> int or None:
        if inverse:
            wo = Endian.Little
        else:
            wo = Endian.Big

        if isinstance(values, list) and len(values) == 2:
            for i in values:
                if not isinstance(i, int):
                    return None
            else:
                decoder = BinaryPayloadDecoder.fromRegisters(values, byteorder=Endian.Big, wordorder=wo)
                return decoder.decode_32bit_uint()
        else:
            return None

    @staticmethod
    def to_uint64(values: list[int], inverse=False) -> int or None:
        if inverse:
            wo = Endian.Little
        else:
            wo = Endian.Big
        if isinstance(values, list) and len(values) == 4:
            for i in values:
                if not isinstance(i, int):
                    return None
                else:
                    decoder = BinaryPayloadDecoder.fromRegisters(values, byteorder=Endian.Big, wordorder=wo)
                    return decoder.decode_64bit_uint()
        else:
            return None

    @staticmethod
    def to_float16(values: int, inverse=False) -> float or None:
        if inverse:
            bo = Endian.Little
        else:
            bo = Endian.Big
        if isinstance(values, int):
            decoder = BinaryPayloadDecoder.fromRegisters([values], byteorder=bo, wordorder=Endian.Little)
            return decoder.decode_16bit_float()
        else:
            return None

    @staticmethod
    def to_float32(values: list[int], inverse=False) -> float or None:
        if inverse:
            wo = Endian.Big
        else:
            wo = Endian.Little
        if isinstance(values, list) and len(values) == 2:
            for i in values:
                if not isinstance(i, int):
                    return None
                else:
                    decoder = BinaryPayloadDecoder.fromRegisters(values, byteorder=Endian.Big, wordorder=wo)
                    return decoder.decode_32bit_float()
        else:
            return None

    @staticmethod
    def to_float64(values: list[int], inverse=False) -> float or None:
        if inverse:
            wo = Endian.Big
        else:
            wo = Endian.Little
        if isinstance(values, list) and len(values) == 4:
            for i in values:
                if not isinstance(i, int):
                    return None
                else:
                    decoder = BinaryPayloadDecoder.fromRegisters(values, byteorder=Endian.Big, wordorder=wo)
                    return decoder.decode_64bit_float()
        else:
            return None
