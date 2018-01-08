#!/usr/bin/env python2
import testsslserver


def main():
    a,b,c = testsslserver.gencert()
    print("%s\n%s\n%s" % (a,b,c))
    for item in [a,b,c]:
        with open(item, 'r') as f:
            print(str(f.read()))
            f.close()
    [testsslserver.cleanup(x) for x in [a,b,c]]


if __name__=="__main__":
    main()

