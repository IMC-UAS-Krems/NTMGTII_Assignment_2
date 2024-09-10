import json
import socket
import inspect
from threading import Thread

SIZE = 1024

class RPCServer:

    def __init__(self, host:str='0.0.0.0', port:int=8080) -> None:
        self.host = host
        self.port = port
        self.address = (host, port)
        self._methods = {}

    def help(self) -> None:
        print('REGISTERED METHODS:')
        for method in self._methods.items():
            print('\t',method)

    def registerMethod(self, function) -> None:
        """
        Pass a method to register all its methods and attributes so they can be used by the client via RPC.
        Arguments:
            function -> the method to register
        """
        try:
            self._methods.update({function.__name__ : function})
        except:
            raise Exception('A non method object has been passed into RPCServer.registerMethod(self, function)')

    def registerInstance(self, instance=None) -> None:
        """
        Pass a instance of a class to register all its methods and attributes so they can be used by the client via RPC.
        Arguments:
            instance -> a class object
        """
        try:
            # Regestring the instance's methods
            for functionName, function in inspect.getmembers(instance, predicate=inspect.ismethod):
                if not functionName.startswith('__'):
                    self._methods.update({functionName: function})
        except:
            raise Exception('A non class object has been passed into RPCServer.registerInstance(self, instance)')

    def __handle__(self, client:socket.socket, address:tuple):
        """
        Pass client connection and its address to perform requests between client and server.
        Arguments:
            client -> the socket to use.
            address -> tuple formed by an ip address and port number
        """
        print(f'Managing requests from {address}.')
        while True:
            try:
                functionName, args, kwargs = json.loads(client.recv(SIZE).decode())
            except: 
                print(f'! Client {address} disconnected.')
                break
            # Showing request Type
            print(f'{address} : {functionName}({args})')
            
            try:
                response = self._methods[functionName](*args, **kwargs)
            except Exception as e:
                # Send back exeption if function called by client is not registred 
                client.sendall(json.dumps(str(e)).encode())
            else:
                client.sendall(json.dumps(response).encode())


        print(f'Completed request from {address}.')
        client.close()
    
    def run(self) -> None:
        """
        Runs the server.
        """
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            self.socket = sock
            sock.bind(self.address)
            sock.listen()

            print('Server running')
            while True:
                try:
                    client, address = sock.accept()

                    Thread(target=self.__handle__, args=[client, address]).start()

                except KeyboardInterrupt:
                    print(f'Server {self.address} interrupted')
                    break

    def shutdown(self):
        """
        Stops the server
        """
        self.socket.close()



class RPCClient:
    def __init__(self, host:str='localhost', port:int=8080) -> None:
        self.__sock = None
        self.__address = (host, port)


    def isConnected(self):
        try:
            self.__sock.sendall(b'test')
            self.__sock.recv(SIZE)
            return True

        except:
            return False


    def connect(self):
        try:
            self.__sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.__sock.connect(self.__address)
        except EOFError as e:
            print(e)
            raise Exception('Client was not able to connect.')
    
    def disconnect(self):
        try:
            self.__sock.close()
        except:
            pass


    def __getattr__(self, __name: str):
        def excecute(*args, **kwargs):
            self.__sock.sendall(json.dumps((__name, args, kwargs)).encode())

            response = json.loads(self.__sock.recv(SIZE).decode())
   
            return response
        
        return excecute

    def __del__(self):
        try:
            self.__sock.close()
        except:
            pass