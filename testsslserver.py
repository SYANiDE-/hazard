#!/usr/bin/env python2
import ssl, socket, time, sys

# Templated server-side sockets-based listener and SSL listener


def listener(host, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind((host, int(port)))
        print("[+] Bound to %s:%s" % (host, port))
        sock.listen(1)
        sx, addr = sock.accept()
        print("[+] Received connection from %s:%s" % (sx.getpeername()[0], sx.getpeername()[1]))
        return sx
    except KeyboardInterrupt:
        print("\n[x] KeyboardInterrupt received.  Exiting.")
        sys.exit()
    except Exception, X:
        # print(str(X))
        pass


def ssllistener(host, port, CERT, PEM):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind((host, int(port)))
        print("[+] Bound to %s:%s" % (host, port))
        sock.listen(5)
        conn, addr = sock.accept()
        context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        context.load_cert_chain(certfile=CERT, keyfile=PEM)
        context.options |= ssl.OP_NO_TLSv1 | ssl.OP_NO_TLSv1_1
        context.set_ciphers('EECDH+AESGCM:EDH+AESGCM:AES256+EECDH:AES256+EDH')
        sx = context.wrap_socket(conn, server_side=True)
        print("[+][SSL] Received connection from %s:%s" % (sx.getpeername()[0], sx.getpeername()[1]))
        return sx, context, sock
    except KeyboardInterrupt:
        print("\n[x] KeyboardInterrupt received.  Exiting.")
        sys.exit()
    except ssl.SSLError as E:
        print(str(E))
    except Exception, X:
        print(str(X))
        # pass


def gencert():
    # https://www.linux.org/threads/creating-a-self-signed-certificate-with-python.9038/
    # https://markusholtermann.eu/2016/09/ssl-all-the-things-in-python/
    from OpenSSL import crypto, SSL
    from pprint import pprint
    from time import gmtime, mktime
    from os.path import exists, join
    from random import choice, randint
    from string import letters
    CN = "SSLS"
    CERT_FILE = "%s.crt" % CN
    PEM_FILE = "%s.pem" % CN
    PUBKEY_FILE = "%s.pub" % CN
    cert_dir = "."
    C_F = join(cert_dir, CERT_FILE)
    K_F = join(cert_dir, PEM_FILE)
    P_F = join(cert_dir, PUBKEY_FILE)
    k = crypto.PKey()
    k.generate_key(crypto.TYPE_RSA, 4096)
    cert = crypto.X509()
    cert.get_subject().C = "".join([choice(letters[:26]) for i in range(2)])
    cert.get_subject().ST = "".join([choice(letters[:26]) for i in range(2)])
    cert.get_subject().L = "".join([choice(letters[:26]) for i in xrange(0, randint(2,32))])
    cert.get_subject().O = "".join([choice(letters[:26]) for i in xrange(0, randint(2,32))])
    cert.get_subject().OU = "".join([choice(letters[:26]) for i in xrange(0, randint(2,32))])
    cert.get_subject().CN = CN
    cert.set_serial_number(randint(1000,9999))
    cert.gmtime_adj_notBefore(0)
    cert.gmtime_adj_notAfter(604800)  # 7 days...
    cert.set_issuer(cert.get_subject())
    cert.set_pubkey(k)
    cert.sign(k, 'sha256')
    open(C_F, 'wt').write(crypto.dump_certificate(crypto.FILETYPE_PEM, cert))
    open(K_F, 'wt').write(crypto.dump_privatekey(crypto.FILETYPE_PEM, pkey=k))
    open(P_F, 'wt').write(crypto.dump_publickey(crypto.FILETYPE_PEM, pkey=k))
    return C_F, K_F, P_F


def cleanup(inp):
    # get rid of the single-use certificates and PKI
    from os.path import exists
    from os import remove
    if exists(inp):
        remove(inp)


def main():
    CERT, PEM, PUBKEY = gencert()
    # sx = listener('127.0.0.1', 13001)
    sx, context, sock = ssllistener('127.0.0.1', 13001, CERT, PEM)
    try:
        while True:
            data = sx.recv(2048)
            if data <> "":
                print(data)
                sx.send("<<< I received your input. (%s)" % ('127.0.0.1'))
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n[x] KeyboardInterrupt received.  Exiting.")
        sx.close()
        [cleanup(x) for x in [CERT, PEM, PUBKEY]]
        sys.exit()
    except:
        pass


    
if __name__=="__main__":
    main()

