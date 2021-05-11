example1 = struct();
example1.command = 'eval';
example1.function = 'disp(''This works.'')';
example1.num_outputs = 0;

example2 = struct();
example2.command = 'feval';
example2.function = 'hSI.startFocus';
example2.inputs = struct(); %define inputs as msg.inputs.input1 = 1; msg.inputs.input2 = 2;
example2.num_outputs = 0;

example3 = struct();
example3.command = 'get';
example3.property = 'hSI.hRoiManager.scanZoomFactor';

example4 = struct();
example4.command = 'set';
example4.property = 'hSI.hRoiManager.scanZoomFactor';
example4.value = 10;

% which example to use:
msg = example1;

% convert struct to json
msg = jsonencode(msg);
fprintf('Sending JSON string: %s\n',msg);
% convert json to byte array
data = unicode2native(msg);

hClient = most.network.tcpip.Client('127.0.0.1',5555);

% first send size of message as a uint64 (8 bytes)
numBytes = numel(data);
numBytes_raw = typecast(uint64(numBytes),'uint8');
hClient.send(numBytes_raw);
% then send data
hClient.send(data);

% read 8 bytes to determine response size
rspNumBytes = typecast(hClient.read(8),'uint64');
rsp = hClient.read(rspNumBytes);
hClient.delete();
rsp = native2unicode(rsp);
fprintf('Received JSON string: %s\n',rsp);