# TODO
# Преоразоваие словаря в json-файл

class HexagonProtocol:
    __id_static: int = 0
    __id: int
    __size: int = 0
    __data: list

    __coding: str = 'utf-8'

    __bytes_start: bytes = b'hexagon'
    __bytes_end: bytes = b'thats all forks'
    __bytes_start_encrypted: bytes = b'hexagon_enc'
    __bytes_end_encrypted: bytes = b'end_enc'
    __bytes_sep: bytes = b':'

    def __init__(self, data: list):
        self.__id = HexagonProtocol.__id_static
        HexagonProtocol.__id_static += 1

        self.__data = data[:]

    def getId(self):
        return self.__id

    def getSize(self):
        return self.__size

    def getData(self):
        return self.__data

    def getByteProtocol(self):
        res_str = self.__createByteStr(self.__bytes_start, self.__bytes_end, self.__bytes_sep)
        return res_str

    def getByteProtocolEncrypted(self):
        return self.__createByteStr(self.__bytes_start_encrypted, self.__bytes_end_encrypted, self.__bytes_sep)

    def __str__(self):
        return 'Object of class HexagonProtocol \n' + \
               'id = ' + str(self.__id) + '\n' + \
               'data = ' + str(self.__data) + '\n'

    def __createByteStr(self, bytes_start, bytes_end, bytes_sep):
        # TODO подсчет size сообщения
        res_str = bytes_start + \
                  str(self.__id).encode(self.__coding) + \
                  bytes_sep + \
                  str(self.__size).encode(self.__coding) + \
                  bytes_sep + \
                  str(self.__data).encode(self.__coding) + \
                  bytes_end

        return res_str

    @staticmethod
    def getDataFromByteStr(byte_str):
        is_HexagonProtocol = True
        if HexagonProtocol.__bytes_start == byte_str[:len(HexagonProtocol.__bytes_start)] and \
                HexagonProtocol.__bytes_end == byte_str[-len(HexagonProtocol.__bytes_end):]:
            # message isn't encrypted
            message = byte_str[len(HexagonProtocol.__bytes_start):-len(HexagonProtocol.__bytes_end)].split(HexagonProtocol.__bytes_sep)
            print(message)

            # TODO проверить размер сообщения

        elif HexagonProtocol.__bytes_start_encrypted == byte_str[:len(HexagonProtocol.__bytes_start_encrypted)] and \
                HexagonProtocol.__bytes_end_encrypted == byte_str[-len(HexagonProtocol.__bytes_end_encrypted):]:
            # message is encrypted
            a = 0
        else:
            is_HexagonProtocol = False

        if not is_HexagonProtocol:
            print('Unknown protocol')
