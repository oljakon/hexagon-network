import socket
import select
import signal
from HexagonProtocol import HexagonProtocol

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

host = '0.0.0.0'
port = 1322
s.bind((host, port))
s.listen(4)
socket_list = [s]

class NetSession:
    players: dict
    max_players: int
    def __init__(self, max_players: int):
        self.players = {}
        self.max_players = max_players

    def IsFull(self):
        return len(self.players) == self.max_players
    
    def AddPlayer(self, sock: socket.socket) -> int:
        if self.IsFull():
            return -1
        else:
            max_id = max(self.players.keys()) if self.players.keys() else -1
            self.players[max_id + 1] = sock
            return max_id + 1
    
    def SendToAll(self, data: dict) -> None:
        byte_str = HexagonProtocol.getByteStrFromData(data)
        for player in self.players:
            self.players[player].send(byte_str)
            
    def SendToOne(self, data:dict, player_id: int) -> None:
        byte_str = HexagonProtocol.getByteStrFromData(data)
        self.players[player_id].send(byte_str)
    
    def SendExceptOne(self, data:dict, player_id: int) -> None:
        byte_str = HexagonProtocol.getByteStrFromData(data)
        for player in self.players:
            if player != player_id:
                self.players[player].send(byte_str)
    
    def __del__(self):
        for player in self.players:
            self.players[player].close()

class NetSessionControl:
    sessions: list
    max_players: int
    def __init__(self, max_players:int):
        self.sessions = []
        self.max_players = max_players
    
    def GetMessage(self, message: dict, sock: socket.socket):
        print(message['type'])
        if message['type'] == 'connect':
            if (len(self.sessions) == 0) or (self.sessions[len(self.sessions) - 1].IsFull()):
                self.sessions.append(NetSession(self.max_players))
            player_id = self.sessions[len(self.sessions) - 1].AddPlayer(sock)
            byte_str = HexagonProtocol.getByteStrFromData({"type": "connect", "session": len(self.sessions) - 1, "player": player_id})
            print(byte_str)
            sock.send(byte_str)
            if self.sessions[len(self.sessions) - 1].IsFull():
                self.sessions[len(self.sessions) - 1].SendToAll({"type": "start"})
        else:
            session_id = message['session']
            sender_id = message['player']
            #protocol = HexagonProtocol({"type": "connect", "session": len(self.sessions) - 1, "player": player_id})
            #byte_str = protocol.getByteProtocol()
            session = self.sessions[session_id]
            session.SendToExceptOne(message, sender_id)
            if message['type'] == 'win':
                del self.sessions[session_id]
                self.sessions[session_id]
        #elif message['']


def sigint_handler(signum, frame):
    global socket_list
    for sock in socket_list:
        sock.close()
    del socket_list
    print('sigint')
    exit(0)

sessions = []

session_control = NetSessionControl(1)

signal.signal(signal.SIGINT, sigint_handler)
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
            
            if data == b'finish':
                sock.close()
                socket_list.remove(sock)
            if data == b'':
                continue
            try:
                d = HexagonProtocol.getDataFromByteStr(data)
                print(d)
                
            except:
                print('Something went wrong')
            else:
                session_control.GetMessage(d, sock)

s.close()
