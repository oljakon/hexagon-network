import json
from sys import getsizeof

example_dict = {'id': 1, 'session_id': 2, 'unit': 'army', 'coord_from': [1, 1], 'coord_to': [10, 10]}

class HexagonProtocol:
    __size: int = 0
    __data: dict

    __coding: str = 'utf-8'

    __bytes_start: bytes = b'hexagon'
    __bytes_end: bytes = b'thats all forks'
    __bytes_sep: bytes = b':'

    def __init__(self, data: dict):
        self.__data = data
        self.__size = getsizeof(data)

    def __str__(self):
        return 'Object of class HexagonProtocol \n' + \
               'data = ' + str(self.__data) + '\n'

    def getSize(self):
        return self.__size

    def getData(self):
        return self.__data

    @staticmethod
    def getByteStrFromData(data: dict) -> bytes:
        res_str = HexagonProtocol.__bytes_start + \
                  HexagonProtocol.__bytes_sep + \
                  json.dumps(data).encode(HexagonProtocol.__coding) + \
                  HexagonProtocol.__bytes_sep + \
                  HexagonProtocol.__bytes_end
        return res_str

    @staticmethod
    def getDataFromByteStr(byte_str: bytes) -> list:
        is_HexagonProtocol = True
        if HexagonProtocol.__bytes_start == byte_str[:len(HexagonProtocol.__bytes_start)] and \
                HexagonProtocol.__bytes_end == byte_str[-len(HexagonProtocol.__bytes_end):]:
            bytes_list = byte_str.split(HexagonProtocol.__bytes_end)
            dict_list = []
            bytes_list.pop(-1)
            for byte_dict in bytes_list:
                byte_dict = byte_dict[len(HexagonProtocol.__bytes_start)+1:-1]
                res = json.loads(byte_dict)
                dict_list.append(res)
            return dict_list

        else:
            is_HexagonProtocol = False

        if not is_HexagonProtocol:
            print('Unknown protocol')
            return []
