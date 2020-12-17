import json

example_dict = {'id': 1, 'session_id': 2, 'unit': 'army', 'coord_from': [1, 1], 'coord_to': [10, 10]}

class HexagonProtocol:
    __size: int = 0
    __data: dict

    __coding: str = 'utf-8'

    __bytes_start: bytes = b'hexagon'
    __bytes_end: bytes = b'thats all forks'
    __bytes_start_encrypted: bytes = b'hexagon_enc'
    __bytes_end_encrypted: bytes = b'end_enc'
    __bytes_sep: bytes = b':'

    def __init__(self, data: dict):
        self.__data = data

    def getSize(self):
        return self.__size

    def getData(self):
        return self.__data

    def getByteProtocol(self):
        return self.__createByteStr(self.__bytes_start, self.__bytes_end, self.__bytes_sep)

    def getByteProtocolEncrypted(self):
        return self.__createByteStr(self.__bytes_start_encrypted, self.__bytes_end_encrypted, self.__bytes_sep)

    def __str__(self):
        return 'Object of class HexagonProtocol \n' + \
               'data = ' + str(self.__data) + '\n'

    def __createByteStr(self, bytes_start, bytes_end, bytes_sep):
        res_str = bytes_start + \
                  bytes_sep + \
                  json.dumps(self.__data).encode(self.__coding) + \
                  bytes_sep + \
                  bytes_end
        return res_str

    @staticmethod
    def getDataFromByteStr(byte_str):
        is_HexagonProtocol = True
        if HexagonProtocol.__bytes_start == byte_str[:len(HexagonProtocol.__bytes_start)] and \
                HexagonProtocol.__bytes_end == byte_str[-len(HexagonProtocol.__bytes_end):]:
            # message isn't encrypted
            message = json.loads(byte_str[len(HexagonProtocol.__bytes_start)+1\
                                          :-len(HexagonProtocol.__bytes_end)-1].decode(HexagonProtocol.__coding))
            return message

        else:
            is_HexagonProtocol = False

        if not is_HexagonProtocol:
            return 'Unknown protocol'
