#!/usr/bin/python

import os
from time import sleep

tests = ["line-key","line-raw","line-norm","bar-clustered",
         "bar-norm-clustered","bar-key-clustered","bar-key-cc","bar-single",
         "box-key","box-time","getter-test"]

for i in tests:
    print("\033[1;31m%s\033[m test !! ============================================" % i)
    os.system('./ep.py -s %s -o %s.pdf' % (i,i))
    print("\033[0;34mfinish !! ============================================\033[m")
    sleep(1)

