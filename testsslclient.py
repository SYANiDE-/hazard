#!/usr/bin/env python2
import ssl, socket, time, sys

# Templated socket-based client and SSL client


def client(host, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((host, int(port)))
        print("[+] connected to %s:%s" % (host, port))
        return sock
    except KeyboardInterrupt:
        print("\n[x] KeyboardInterrupt received.  Exiting.")
        sys.exit()
    except Exception, X:
        # print(str(X))
        pass


def sslclient(host, port):
    try:
        from os.path import join
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        context.options |= ssl.OP_NO_TLSv1 | ssl.OP_NO_TLSv1_1 
        sslsock = context.wrap_socket(sock, server_hostname=host)
        sslsock.connect((host, int(port)))
        print("[+][SSL] Connected to %s:%s" % (host, port))
        return sslsock
    except KeyboardInterrupt:
        print("\n[x] KeyboardInterrupt received.  Exiting.")
        sys.exit()
    except ssl.SSLError as e:
        print(str(e))
    except Exception, X:
        print(str(X))
        # pass


def main():
    # cx = client('127.0.0.1', 13001)
    cx = sslclient('127.0.0.1', 13001)
    try:
        while True:
            cx.send("<<< Touching base from client %s" % '127.0.0.1')
            data = cx.recv(2048)
            if data <> "":
                print(data)
            time.sleep(3)
    except KeyboardInterrupt:
        print("\n[x] KeyboardInterrupt received.  Exiting.")
        cx.close()
        sys.exit()
    except:
        pass


if __name__=="__main__":
    main()


