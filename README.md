# Python client for ScanImage remote stimulation control - Histed lab

This is a very simple Python client that can control ScanImage remotely over a network socket.  We use it to change photostimulation power, but it can be used to adjust imaging power, run imaging series, etc.

The Scanimage/Matlab side server code will be part of a coming Vidrio release.
This is called "JsonServer" because it uses json strings to send commands, allowing Python and Matlab to share data.  The Matlab/Scanimage "AsyncServer.m", in scanimage in +most/+network/+tcpip, uses Matlab APIs and requires Matlab on both sides.

All tested with a Python 3.8 environment (not provided)

Please feel free to reach out with questions about how to use this: mark.histed@nih.gov.

## Files
  - py_json_client.py - the Python client. provided.)
  - dummy_json_server.py - a Python fake/dummy implementation of the Vidrio JsonServer.m, which allows unit testing
  - test_dummy_py_jsonserver.m - run tests against the dummy python server
  - test_matlab_jsonserver.py - run tests against the real Scanimage Matlab server, requires Matlab and a Scanimage setup

## Testing, on one machine with the dummy Python server

    - in one window, run python dummy_json_server.py
    - in another, run python test_dummy_py_jsonserver.py

## Testing to scanimage machine

    - run JsonServer.m in Matlab  (need to addpath the root scanimage path)
    - python test_matlab_jsonserver.py

## Contact

mark.histed@nih.gov
