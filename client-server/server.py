import socket
import select
import signal
from HexagonProtocol import HexagonProtocol

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


host = ''
port = 8007
s.bind((host, port))
s.listen(4)
socket_list = [s]


def sigint_handler(signum, frame):
    global socket_list
    for sock in socket_list:
        sock.close()
    del socket_list
    exit(0)


while 1:
    #print("sl = ", socket_list)
    signal.signal(signal.SIGINT, sigint_handler)
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
        


s.close()