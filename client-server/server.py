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
    r,w,e = select.select(socket_list, [], [])

    #print(r, w, e)
    for read in r:
        #print(r, read == s)
        if read == s:
            conn, addr = s.accept()
            socket_list.append(conn)
        else:
            #conn = None
            data = ''
            data = read.recv(1000000)
            print('client', data)
            read.send(data)
        
            if data == b'finish':
                read.close()
                socket_list.remove(read)
               

            try:
                HexagonProtocol.getDataFromByteStr(data)
            except:
                print('Something went wrong')
        


