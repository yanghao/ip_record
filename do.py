import time
import socket
import logging
from urllib.request import urlopen

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger("main")
fh = logging.FileHandler("log.txt")
log.addHandler(fh)
server = ["192.168.0.10", 8080]
hostname = socket.gethostname()

delta = 30

last = 0
while True:
    now = time.time()
    if (now - last) > delta:
        try:
            log.info("now ...")
            server_and_name = server + [hostname]
            log.info(server_and_name)
            content = urlopen("http://%s:%d/%s" % tuple(server_and_name)).read()
            log.info(b"content: %s" % content)
        except:
            log.info("access to %s:%d failed" % server)
        last = now
    else:
        time.sleep(5)
