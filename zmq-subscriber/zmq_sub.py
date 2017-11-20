import sys
import zmq

port = "28332"

context = zmq.Context()
socket = context.socket(zmq.SUB)

print "Collecting updates from zmq socket..."
socket.connect ("tcp://localhost:%s" % port)
socket.setsockopt(zmq.SUBSCRIBE, '') #Messages can be filtered here -> 'rawtx'

while(1):
  string = socket.recv()
  print string

