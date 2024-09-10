# Networking Technologies and Management Systems II

## Assignment 2 (e-learning): RPC

We have briefly touched Remote Procedure Calls (RPCs) in class. Since the best way of understanding RPCs is to code one yourself, this assignment (e-learning session) will show you how to implement one.

## Instructions

Take a look at the source code provided:

- `rpc.py` contains the implementation of the classes `RPCServer` and `RPCClient`. These two classes implement a general-purpose RPC protocol using JSON payloads.
  - `RPCServer` provides a way of **registering** arbitrary Python methods on the server side (the methods that will be executed when the client invokes them).
  - `RPCClient` is the class that the client uses to connect to the server and invoke a method (the client needs to know in advance which method to invoke and how to invoke it - we will leave this problem for Distributed Systems in the 4. semester).
- `rpc_server.py` implements a sample server that provides two functions: `add` and `sub`.
- `rpc_client.py` implements a client that invokes both example functions.

Now that you understand how the code works, you have the following tasks:

1. Implement on the server side a function `fibonacci` that takes a positive integer `n` as a parameter. This function will calculate the n-th Fibonacci number: a_n = a_{n-1} + a_{n_2}.
   - Don't forget to add error handling for those cases where the input is not valid!

2. Modify the client to call that function with several values of `n` (both valid and invalid). If a value is invalid, the client will return the string `invalid input`.
3. Create a new function on the server side that calculates and returns the **checksum** of the byte array provided as parameter (see Assignment 1). Modify the client to call the function using several example calls.

