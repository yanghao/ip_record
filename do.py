import re
import time
import socket
import logging
from urllib.request import urlopen
from urllib.error import HTTPError, URLError
from socket import timeout
from subprocess import check_output

def get_ip_list():
    output = check_output("ifconfig")
    output = output.decode()
    p = re.compile('inet ([0-9]+\.[0-9]+\.[0-9]+\.[0-9]+)')
    ip_list = []
    for line in output.split('\n'):
        m = p.search(line)
        if m:
            ip = m.groups()[0]
            if not ip.startswith("127"):
                ip_list.append(ip)
    return ip_list

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger("main")
fh = logging.FileHandler("log.txt")
log.addHandler(fh)
server = ["xiaoyezi.org", 8080]
hostname = socket.gethostname()

delta = 30

last = 0
n = 0
while True:
    now = time.time()
    if (now - last) > delta:
        try:
            ip_list = get_ip_list()
            log.info("ip list: %s" % str(ip_list))
            for ip in ip_list:
                server_and_name = server + [hostname+"/"+ip]
                log.info(server_and_name)
                try:
                    content = urlopen("http://%s:%d/%s" % tuple(server_and_name), timeout=10).read()
                    log.info(b"content: %s - %d" % (content, n))
                    n += 1
                except (HTTPError, URLError) as error:
                    log.error('Data not retrieved because: %s', error)
                except timeout:
                    log.error('socket timed out')
                else:
                    log.info('Access successful.')
        except:
            log.info("access to %s:%d failed" % server)
        last = now
    else:
        time.sleep(5)
