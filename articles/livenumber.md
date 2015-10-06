---
layout: page
permalink: "livenumber.html"
title:  "增加直播间人数 - 加强版"
---

## 事前唠个叨

这个项目实际上是我一开始听到别人说b站的弹幕姬在连接服务器后会被算成一个观众，而且现在有很多人被联系问要不要刷人数，这引起了我的兴趣。

经过三种弹幕姬代码的反复对比，最终发现b站是使用 **WebSocket** 进行的弹幕连接和获取。

于是<del>跪着</del>请 *cnBeining* 写了一个 Python 版本的 WebSocket 连接器，又<del>厚颜无耻</del>的让他加上了一个 HTTP Proxy 功能……

但是这个黑科技<del>在我的肆意使用下</del>失效了，然后便一直是失效的……

突然发现typcn已经在他的Gist上改进了！并且CPU占用率<del>极高</del>极低，带30秒心跳。

### 源码如下：

{% highlight python %}
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
{% endhighlight %}

嘛，开包即用，效果良好。大家可以在[这里](/script/live_number.py)或者 [Github](https://gist.github.com/typcn/cd87a471e0575a6785b9) 上找到源码。

##用法

{% highlight bash %}
~ $ python live_number.py -c 12450 -t 500

-h 帮助  
-c 房间号（放肆！）  
-t 增加的人数
{% endhighlight %}

***

就是这样，点开导航栏中的 *typcn* 页面，你会发现更多有趣的东西~
