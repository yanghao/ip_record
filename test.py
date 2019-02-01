import os
import time
import bjoern

from time import gmtime, strftime

DATA_PATH = "static"

def app(env, start_response):
    start_response('200 OK', [])
    path = env["PATH_INFO"]
    fn = os.path.basename(path)
    #print("path: %s" % path)
    ip = env["REMOTE_ADDR"]
    ip = ip.encode('utf-8')
    path = path[1:] # strip out starting /
    if path:
        parent = os.path.dirname(path)
        path = os.path.join(DATA_PATH, parent)
        if not os.path.isdir(parent):
            os.system("mkdir -p %s" % path)
        path = os.path.join(path, fn)
        print("got: %s" % path)
        with open(path, "wb") as fd:
                ts = strftime("%Y-%m-%d %H:%M:%S +0000", gmtime())
                ts = ts.encode('utf-8')
                fd.write(b"%s @ %s\n" % (ip, ts))
        return b"OK"
    else:
        r = []
        for root, dirs, files in os.walk(DATA_PATH):
            for f in files:
                tmp = b"%s/%s: " % (root.encode('utf-8'), f.encode('utf-8'))
                with open(os.path.join(root, f), "rb") as fd:
                    tmp += fd.read()
                r.append(tmp)
        r.sort()
        #print("put: %s" % r.decode('utf-8'))
        return b''.join(r)

if __name__ == '__main__':
    if not os.path.isdir(DATA_PATH):
        os.system("mkdir -p %s" % DATA_PATH)
    bjoern.run(app, '0.0.0.0', 8080)
