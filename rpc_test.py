import pytest
import time

from rpc import RPCClient, RPCServer
from rpc_server import fibonacci

from multiprocessing import Process

@pytest.fixture
def setup_server():
    server = RPCServer()
    server.registerMethod(fibonacci)

    server_process = Process(target=server.run)
    server_process.start()

    time.sleep(1)

    server_address = '127.0.0.1'
    yield server_address

    server_process.terminate()
    server_process.join()


def test_fibonacci(setup_server):
    client = RPCClient(setup_server, 8080)
    client.connect()
    assert client.fibonacci(8) == 21
    assert client.fibonacci(3) == 2
    assert client.fibonacci(0) == 0
    assert client.fibonacci(-1) == "invalid input"
    client.disconnect()



    
