"""Python client to talk to a remote Scanimage TCP/IP server

Requires Py3.7 or later

210329: MH: created

Mark Histed mark.histed@nih.gov

# todo: currently using little-endian byte order, should really be big
"""

import socket
import json

class ServerError(RuntimeError):
    pass


class ScanimageTcpipClient:
    """
    Notes: Can be called as a context manager using with statement
    """
    # todo
    # TCP_NODELAY

    def __init__(self, address='127.0.0.1', port=5555):
        self.address = address
        self.port = port

        self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)  # TCP_NODELAY turns off buffering
        self._sock.settimeout(0.100)  # 100ms timeout, blocking mode
        self._sock.connect((address, port))

    def close(self):
        self._sock.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Call close, don't return anything, let exceptions propagate"""
        self._sock.close()

    ### methods

    def _send_cmd(self, send_cmd_dict):
        """Convert to json for network, then send 8-byte length, then bytes command"""
        send_bytes = json.dumps(send_cmd_dict).encode('utf-8')
        self._sock.sendall(len(send_bytes).to_bytes(8, byteorder='little'))
        self._sock.sendall(send_bytes)


    def _read_result(self):
        """Reads 8-byte length, then string command, then json decodes and returns obj.
        """
        respLen = int.from_bytes(self._sock.recv(8), byteorder='little')  # encoded in 8 bytes
        #print(respLen)
        respData = self._sock.recv(respLen)
        #print(respData)
        respO = json.loads(respData)  # loads() can read utf-8 bytes directly

        if 'error' in respO:
            raise ServerError(respO['error'])

        return respO


    def si_get(self, serv_var):
        """
        pseudocode:
            # create message dict
            # make json
            # convert to bytes
            # send message
            # read 8 bytes
            # read full response
            # convert to text
            # un json
            # return object
        """
        self._send_cmd({'command': 'get', 'property': serv_var})
        respO = self._read_result()
        return respO['value']


    def si_set(self, serv_var, value):
        """
        Returns:
            None
        """
        self._send_cmd({'command': 'set', 'property': serv_var, 'value': value})
        respO = self._read_result()
        assert respO['value'] == value, 'return on set should be identical to requested new value: bug?'


    def si_eval(self, eval_str, num_outputs):
        """Eval a string on server in Matlab
        Args: 
            num_outputs: must be specified"""

        self._send_cmd({'command': 'eval', 'function': eval_str, 'num_outputs': num_outputs})
        respO = self._read_result()
        assert len(respO['outputs']) == num_outputs, 'unexpected number of outputs'
        if num_outputs > 0:
            return([respO['outputs'][k] for k in respO['outputs']])
        

    def si_feval(self, feval_str, num_outputs, inputs=[]):
        """feval form. 
        Args:
            inputs: list of inputs to be passed to feval'd function"""
        inputD = { 'in%03d'%ik: k for ik,k in enumerate(inputs) }
        self._send_cmd({'command': 'feval', 'function': feval_str,
                        'inputs': inputD, 'num_outputs': num_outputs})
        respO = self._read_result()
        assert len(respO['outputs']) == num_outputs, 'unexpected number of outputs'
        if num_outputs > 0:
            return([respO['outputs'][k] for k in respO['outputs']])
