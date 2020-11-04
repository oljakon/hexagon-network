import socket
from time import sleep
from HexagonProtocol import HexagonProtocol

#################################
a = HexagonProtocol([123, 123, 'aa'])
string_a = a.getByteProtocol()

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = 'localhost'
port = 8007
s.connect((host, port))
# s.send(string_a)

s.send(bytes('hello', encoding='utf-8'))

data = s.recv(1000000)

print('received', data.decode(encoding='utf-8'), len(data), 'bytes')

sleep(3)
s.send(bytes('finish', encoding='utf-8'))
s.close()
################################

# print(type([]))
# a = HexagonProtocol([123, 123, 'aa'])
# b = HexagonProtocol([])
# print(a.getId(), b.getId())
# print(a)
# print(a.getByteProtocol())
# string_a = a.getByteProtocol()

# HexagonProtocol.getDataFromByteStr(string_a)

###############################

# print('привет 12'.encode('utf-8').hex())
# print(bytes.fromhex('d0bfd180d0b8d0b2d0b5d182203132').decode('utf-8'))