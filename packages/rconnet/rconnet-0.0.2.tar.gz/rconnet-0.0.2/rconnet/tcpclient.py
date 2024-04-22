import hashlib
import socket
import time
import logging

class TCPClientException(Exception):
    pass

class TCPClientStatuses:
    DISABLED = 0
    CONNECTED = 1
    RECONNECTING = 2

class TCPClient(object):

    def __init__(self, address: str,
                 password: int,
                 port: int=4711,
                 debug: bool=True,
                 debug_format: str="%(levelname)s:%(message)s",
                 debug_level: object=logging.DEBUG,
                 on_connect = None,
                 on_disconnect = None,
                 on_close = None,
                 on_status = None,
                 ):

        self.socket = None
        self.address = address
        self.password = password
        self.port = port
        self.debug = debug
        self.debug_format = debug_format
        self.debug_level = debug_level
        self.on_connect = on_connect,
        self.on_disconnect = on_disconnect,
        self.on_close = on_close,
        self.on_status = on_status,
        self._status = TCPClientStatuses.DISABLED
        self._inr = 0

        logging.basicConfig(format=self.debug_format, level=self.debug_level)

    def _exec_event(self, name, *args):
        method = getattr(self, name)
        if type(method) == tuple: method = method[0]
        if method is not None: method(*args)

    def log(self, *value):
        if self.debug: logging.debug(" ".join(str(v) for v in value))

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, status):
        self._status = status
        self._exec_event("on_status", status)

    def start(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.address, self.port))
        self._pre_init()
        self.status = TCPClientStatuses.CONNECTED
        self._exec_event("on_connect")
        return True

    def _pre_init(self):
        self.pre_init()

    def pre_init(self):
        welcResponse = ""
        while 1:
            data = self.socket.recv(1024)
            welcResponse += data.decode("utf-8")
            eosPos = welcResponse.find('\n\n')
            if eosPos != -1: break;

        prefix = '### Digest seed: '
        seedPos = welcResponse.find(prefix)
        seed = ""

        if seedPos == -1: raise Exception("Authorization is not possible")

        seedPos += len(prefix)
        seedPosEnd = welcResponse.find('\n', seedPos)
        seed = welcResponse[seedPos:seedPosEnd].encode("utf-8")

        md5Obj = hashlib.md5()
        md5Obj.update(seed)
        md5Obj.update(self.password.encode("utf-8"))
        passHash = md5Obj.hexdigest()

        self.socket.send(('\x02' + 'login ' + passHash + '\n').encode("utf-8"))
        data = self.socket.recv(1024).decode("utf-8")
        if "Authentication successful, rcon ready." not in data: raise Exception(data)

    def is_closed(self):
        return self.status == TCPClientStatuses.DISABLED

    def close(self):
        if not self.socket: return None
        self.status = TCPClientStatuses.DISABLED
        self.socket.close()
        self._exec_event("on_close")

    def rcon_invoke(self, command):
        if not self.socket: raise Exception("The client is not connected")
        self.socket.send(('\x02' + command + '\n').encode("utf-8"))
        self._inr += 1
        result = ""
        done = False
        while not done:
            try:
                data = self.socket.recv(2048)
                if data is None: raise Exception("Client has terminated the current connection. ")
            except Exception as error:
                self.status = TCPClientStatuses.DISABLED
                self._exec_event("on_disconnect", error)
                raise Exception(error)
            for c in data:
                if c == 0x4:
                    done = True
                    break
                result += chr(c)
        if len(result) > 0 and result[-1] == "\n": result = result[:-1]
        if result.strip() == "": return None
        return result

class TCPListener(TCPClient):

    def __init__(self, *args, commands:list = [], on_recv:object = None, **kwargs):
        super().__init__(*args, **kwargs)
        self._commands = commands
        self.on_recv = on_recv

    def pre_init(self):
        super().pre_init()
        for command in self._commands:
            self.socket.send(('\x02' + command + '\n').encode("utf-8"))

    def start(self):
        while True:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            try:
                self.socket.connect((self.address, self.port))
                self._pre_init()
                self.status = TCPClientStatuses.CONNECTED
                self._exec_event("on_connect")
            except Exception as error:
                time.sleep(3)
                print(error)
                continue

            while 1:
                try:
                    data = self.socket.recv(2048)
                    if data is None: raise Exception("Client has terminated the current connection. ")
                except Exception as error:
                    self._exec_event("on_disconnect", error)
                    break
                result = data
                done = False
                if result[-1] == 0x4: done = True
                while not done:
                    data = self.socket.recv(2048)
                    for c in data:
                        if c == 0x4:
                            done = True
                            break
                        result += chr(c)
                self._exec_event("on_recv", result)
