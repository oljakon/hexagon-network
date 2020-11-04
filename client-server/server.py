import socket
import select
from HexagonProtocol import HexagonProtocol

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = ''
port = 8007
s.bind((host, port))
s.listen(4)
socket_list = [s]


while 1:
    #print("sl = ", socket_list)
    sockets_to_read, _, _ = select.select(socket_list, [], [])

    #print(r, w, e)
    for sock in sockets_to_read:
        #print(r, read == s)
        if sock == s:
            conn, addr = s.accept()
            socket_list.append(conn)
        else:
            #conn = None
            data = ''
            data = sock.recv(1000000)
            print('client', data)
            sock.send(data)
        
            if data == b'finish':
                sock.close()
                socket_list.remove(sock)
               

            try:
                HexagonProtocol.getDataFromByteStr(data)
            except:
                print('Something went wrong')
        


