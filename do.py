import time
import socket
from urllib.request import urlopen

server = ["192.168.0.10", 8080]
hostname = socket.gethostname()

delta = 30

last = 0
while True:
    now = time.time()
    if (now - last) > delta:
        try:
            print("now ...")
            server_and_name = server + [hostname]
            print(server_and_name)
            content = urlopen("http://%s:%d/%s" % tuple(server_and_name)).read()
            print(b"content: %s" % content)
        except:
            print("access to %s:%d failed" % server)
        last = now
    else:
        time.sleep(5)
