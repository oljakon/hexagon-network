import socket
from HexagonProtocol import HexagonProtocol

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = 'localhost'
port = 8007
s.bind((host, port))
s.listen(4)

while 1:
    conn, addr = s.accept()
    data = conn.recv(1000000)
    print('client is at', addr, data)
    conn.send(data)

    if data == b'finish':
        break

    try:
        HexagonProtocol.getDataFromByteStr(data)
    except:
        print('Something went wrong')

conn.close()
