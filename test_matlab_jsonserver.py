"""test script for the python scanimage software"""

from py_json_client import ScanimageTcpipClient
import sys

#address = '127.0.0.1'
address = '10.150.6.93'

with ScanimageTcpipClient(address=address) as tc:
    print(tc.si_get('s'))
    tc.si_set('testfield', 'a value')
    print(tc.si_get('testfield'))
    tc.si_set('testfield', {'new_value_dict': 1})
    print(tc.si_get('testfield'))

    tc.si_eval('disp("This works.")', 0)
    out = tc.si_eval('sqrt(20)', 1)
    print (f'eval: hould be 4.47, sqrt(20): {out[0]:.3g}')

    out = tc.si_feval('sqrt', 1, inputs=[20])
    print (f'feval: should be 4.47, sqrt(20): {out[0]:.3g}')

sys.exit(0)

# ScanImage testing
with ScanimageTcpipClient(address=address) as tc:
    #tc.si_eval('disp("This works.")', 0)
    #tc.si_feval('hSI.startFocus', params=(1,2)) # not sure how to implement
    print(tc.si_get('s'))
    print(tc.si_get('hSI.hRoiManager.scanZoomFactor'))
    #tc.si_set('hSI.hRoiManager.scanZoomFactor', value=10)
    print(tc.si_get('hSI.hRoiManager.scanZoomFactor'))
