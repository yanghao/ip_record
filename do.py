import time
import socket
from urllib.request import urlopen

hostname = socket.gethostname()

delta = 30

last = 0
while True:
    now = time.time()
    if (now - last) > delta:
        try:
            print("now ...")
            content = urlopen("http://192.168.0.18:8080/%s" % hostname).read()
            print(b"content: %s" % content)
        except:
            print("access to 192.168.0.18:8080 failed")
        last = now
    else:
        time.sleep(5)
