#!/usr/bin/env python3
import os,sys, socket, pty


def main():
	if not len(sys.argv) == 4:
		print("Simple socket-based bind server; serve an arbitrary program")
		print("USAGE: ./%s <prog> <ip> <port>" % sys.argv[0])
		sys.exit()
	self,prog,ip,port = sys.argv
	sx = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	sx.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
	sx.bind((ip,int(port)))
	sx.listen(1)
	(cx,addr) = sx.accept()
	os.dup2(cx.fileno(),2)
	os.dup2(cx.fileno(),1)
	os.dup2(cx.fileno(),0)
	try:
		pty.spawn("%s" % prog)
	except:
		cx.close()
		sx.close()
	cx.close()
	sx.close()

if __name__=="__main__":
	main()
