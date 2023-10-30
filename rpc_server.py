from rpc import RPCServer

def add(a, b):
    return a+b

def sub(a, b):
    return a-b

##########################################################
# Implement your server-side functions HERE
##########################################################


server = RPCServer()

server.registerMethod(add)
server.registerMethod(sub)

##########################################################
# Register other methods
##########################################################

server.run()

