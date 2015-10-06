#!/usr/bin/env python
#coding:utf-8
# Author:  Beining --<cnbeining#gmail.com>
# Author:  TYPCN --<typcncom#gmail.com> ( Performance improve and fix )
# Purpose: A simple script to get lots of viewers of Bilibili Live
# Created: 08/11/2015
# Error report: http://www.cnbeining.com/?p=952
# https://github.com/cnbeining  somewhere within my gists

import sys
import time
import getopt
from multiprocessing import Process
import binascii
import random
import re
import traceback
import socket
from threading import Thread
from multiprocessing.pool import ThreadPool

global proxy_list

#----------------------------------------------------------------------
def fake_connector(cid, is_proxy = False):
    """"""
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.connect(("livecmt.bilibili.com",88))
    handshake = "0101000c0000%04x00000000" % int(cid)
    s.send(binascii.a2b_hex(handshake))
    while 1:
        time.sleep(29)
        s.send(binascii.a2b_hex("01020004"))

#----------------------------------------------------------------------
def main(cid, thread_number, is_proxy = False):
    pool = ThreadPool(int(thread_number))
    for x in range(0, thread_number*10):
        pool.apply_async(fake_connector,[cid, is_proxy])
    pool.close()
    time.sleep(99999999)

#----------------------------------------------------------------------
def usage():
    """"""
    print('''Use as:
    -c: cid, room number
    -t: thread number

    You can use Tor and proxychains or others to proxy
    Press Ctrl+C to exit.
    ''')

if __name__=='__main__':
    is_proxy = False
    argv_list = sys.argv[1:]
    try:
        opts, args = getopt.getopt(argv_list, "hc:t:",
                                   ['help', "cid=", 'thread_number='])
    except getopt.GetoptError:
        usage()
        exit()
    for o, a in opts:
        if o in ('-h', '--help'):
            usage()
            exit()
        if o in ('-c', '--cid'):
            cid = a
        if o in ('-t', '--thread_number'):
            thread_number = int(a)
    if is_proxy:
        proxy_list = proxy_file_to_list(proxy_file)
    print('Getting room {cid} {thread_number} viewers...'.format(cid = cid, thread_number = thread_number))
    main(cid, thread_number, is_proxy)