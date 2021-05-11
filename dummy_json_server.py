"""Python server that acts as a dummy ScanImage TcpIp server.
Receives messages and commands, prints them to stdout.

The 
get and set commands can modify and return values from valuesD - you can set that dict to give initial defaults.
eval and feval commands do nothing but print their payload.

- 210330 MH: created.  
"""

import argparse
import socketserver
import socket
import threading
import json

    
parser = argparse.ArgumentParser(description='Dummy server in python for ScanImage TCP/IP server')
parser.add_argument('--address', '-a', type=str, default='127.0.0.1')
parser.add_argument('--port', '-p', type=int, default=5555)

args = parser.parse_args()

initValuesD = {
    's': 'i_am_a_server',
    'testfield': 1 }
                  

class ScanImageDummyRequestHandler(socketserver.BaseRequestHandler):
    """Class to handle messages and print them"""
    #TODO: check for TCP_NODELAY?

    
    def handle(self):
        # get the length
        # get the message
        # un-json
        # switch/print
        # return the correct value
        # done

        print(f'** Got a connection, from {self.client_address}')

        while True:
            # handle multiple commands before tearing down the request class
            r0 = self.request.recv(8)
            if len(r0) == 0:
                print(f'** Connection closed')
                return
            respLen = int.from_bytes(r0, byteorder='little')
            respData = self.request.recv(respLen)
            respO = json.loads(respData)
            #print(respO)

            if respO['command'] == 'set':
                print(f"set: {respO['property']} = {repr(respO['value'])}")
                self.server._valuesD[respO['property']] = respO['value'] # change value in valuesD
                respO['actual'] = respO['value']
                self._send_cmd(respO)

            elif respO['command'] == 'get':
                if respO['property'] in self.server._valuesD:
                    val = self.server._valuesD[respO['property']]
                else:
                    val = 'None'
                print(f"get: {respO['property']} -- returning value {repr(val)}")
                respO['value'] = val
                self._send_cmd(respO)            

            elif respO['command'] == 'eval' or respO['command'] == 'feval':
                if respO['num_outputs'] == 0:
                    outputStr = ''
                else:
                    outputStr = f"[outputs{{1:{respO['num_outputs']}}}] = "
                print(f"{respO['command']}: {outputStr}{respO['function']}")
                # package (fake) outputs and send back
                outputD = { 'output%d'%(k+1): 'dummyvalue%d'%(k+1) for k in range(respO['num_outputs'])}
                respO['outputs'] = outputD
                self._send_cmd(respO)

            else:
                raise RuntimeError(f"Invalid command {respO['command']}")
            

    def _send_cmd(self, send_cmd_dict):
        """Convert to json for network, then send 8-byte length, then bytes command"""
        send_bytes = json.dumps(send_cmd_dict).encode('utf-8')
        #print(send_bytes)
        self.request.sendall(len(send_bytes).to_bytes(8, byteorder='little'))
        self.request.sendall(send_bytes)



################################################################        

    
if __name__ == '__main__':
    with socketserver.TCPServer((args.address, args.port), ScanImageDummyRequestHandler) as server:
        # note this is a synchronous server: waits for connection, handles it (can have many commands),
        # waits for another, etc.  exits on Ctrl-C.
        print(f'Starting server... done.  Listening on {args.address} port {args.port}.')
        server._valuesD = initValuesD # load the values into the server so the handler can access them
        #server.socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)  # TCP_NODELAY turns off buffering
        #server.socket.settimeout(0.100)  # 100ms timeout, blocking mode
        server.serve_forever()  # can handle many connections in sequences, each with several possible commands







