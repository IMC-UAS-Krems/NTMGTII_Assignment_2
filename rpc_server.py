from rpc import RPCServer

def add(a, b):
    return a+b

def sub(a, b):
    return a-b

##########################################################
# Implement your server-side functions HERE
##########################################################


if __name__ == "__main__":
    server = RPCServer()

    server.registerMethod(add)
    server.registerMethod(sub)

    ##########################################################
    # Register other methods
    ##########################################################

    server.run()

