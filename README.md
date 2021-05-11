## Python client usage

   ````from py_json_client import ScanimageTcpipClient````

Tested with a Python 3.8 environment:
        - conda activate 457nmControlTestPy38  (yml in 457nmControl repo)

## Testing, on one machine with the dummy Python server

    - in one window, run python dummy_json_server.py
    - in another, run python test_dummy_py_jsonserver.py

## Testing to scanimage machine

    - run JsonServer.m in Matlab  (need to addpath the root scanimage path)
    - python test_matlab_jsonserver.py

## Contact

mark.histed@nih.gov
