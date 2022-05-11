import globalStart
import client
import zmq

if __name__ == "__main__":
    globalStart.gStart(-1)

    defaultAddr = '2345'
    ctx = zmq.Context()
    sock = ctx.socket(zmq.SUB)
    sock.connect("tcp://127.0.0.1:"+defaultAddr)
    sock.subscribe("")  # Subscribe to all topics

    msg = sock.recv_string()

    if msg=='a':
        print("Success!")