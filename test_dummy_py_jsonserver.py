"""test script for the python scanimage software"""

from py_json_client import ScanimageTcpipClient
import sys
import time

address = '127.0.0.1'

with ScanimageTcpipClient(address=address) as tc:
    print(f"getting s: {tc.si_get('s')}")
    tc.si_set('testfield', 'a value')
    print(f"getting testfield: {tc.si_get('testfield')}")
    tc.si_set('testfield', {'new_value_dict': 1})
    print(f"getting testfield: {tc.si_get('testfield')}")    

    tc.si_eval('disp("This works.")', 0)
    out = tc.si_eval('sqrt(20)', 1)
    print (f'eval: should be 4.47, sqrt(20): {out[0]}')

    out = tc.si_feval('sqrt', 1, inputs=[20])
    print (f'feval: should be 4.47, sqrt(20): {out[0]}')


sys.exit(0)

