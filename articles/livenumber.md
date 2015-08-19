---
layout: page
permalink: "livenumber.html"
title:  "增加直播间人数"
---

## 事前唠个叨

这个项目实际上是我一开始听到别人说b站的弹幕姬在连接服务器后会被算成一个观众，而且现在有很多人被联系问要不要刷人数，这引起了我的兴趣。

经过三种弹幕姬代码的反复对比，最终发现b站是使用 **WebSocket** 进行的弹幕连接和获取。

于是<del>跪着</del>请 *cnBeining* 写了一个 Python 版本的 WebSocket 连接器，又<del>厚颜无耻</del>的让她加上了一个 HTTP Proxy 功能……

### 源码如下：

{% highlight python %}
#!/usr/bin/env python
#coding:utf-8
# Author:  Beining --<cnbeining#gmail.com>
# Purpose: A simple script to get lots of viewers of Bilibili Live
# Created: 08/11/2015
# Error report: http://www.cnbeining.com/?p=952
# https://github.com/cnbeining  somewhere within my gists

import sys
import time
import getopt
from multiprocessing import Process
from websocket import create_connection, WebSocketConnectionClosedException, WebSocketProxyException, WebSocketException
import random
import re
import traceback
import socket

global proxy_list

#----------------------------------------------------------------------
def fake_connector(cid, is_proxy = False):
    """"""
    try:
        if is_proxy:
            proxy_server = random.choice(proxy_list)
            host, port = proxy_server.split(':')
            ws = create_connection('ws://livecmt.bilibili.com:88/{cid}'.format(cid = cid), http_proxy_host = host, http_proxy_port = int(port))
        else:
            ws = create_connection('ws://livecmt.bilibili.com:88/{cid}'.format(cid = cid))
        while 1:
            time.sleep(5)
            a = ws.recv()
    except (WebSocketProxyException, socket.error, TypeError):  #proxy server died
            #/usr/local/lib/python2.7/site-packages/websocket/_http.py L186 WTF????
        print(proxy_server + ' died!')
        try:
            proxy_list.remove(proxy_server)
        except Exception, err:
            print(traceback.format_exc())
    except (WebSocketConnectionClosedException, WebSocketException):
        return -1
    except Exception, err:
        print(traceback.format_exc())
        return 0
    finally:
        return

#----------------------------------------------------------------------
def main(cid, thread_number, is_proxy = False):
    """"""
    #Get a list of threads
    process_list = [Process(target=fake_connector, args=((cid, is_proxy, ))) for i in xrange(int(thread_number))]  #Queue? Your ass
    [i.start() for i in process_list]  #ignite every one
    try:
        while 1:
            alive_list = [i.is_alive() for i in process_list]
            print('Active thread: ' + str(len(alive_list)))
            death_position_list = [i for i, x in enumerate(alive_list) if x == False]
            if len(death_position_list) > 0:  #someone died
                print('Some died, adding {COUNT} new threads'.format(COUNT = len(death_position_list)))
                for i in death_position_list:
                    del process_list[i]  #remove body
                    process_list.append(Process(target=fake_connector, args=((cid, is_proxy, ))))
                    process_list[-1].start()  #ignite
            time.sleep(3)
    except Exception as e:
        print(e)
        for i in process_list:
            try:
                i.terminate()  #ensure safe exit
            except:
                pass
        exit()

#----------------------------------------------------------------------
def proxy_file_to_list(proxy_file):
    """fileIO->list
    file:
    112.20.190.135:80
    223.151.86.8:9000
    171.36.67.213:8090
    124.202.168.26:8118
    219.133.31.120:8888
    
    list:
    ['112.20.190.135:80', '223.151.86.8:9000', '171.36.67.213:8090',...
    """
    final_list = []
    pattern = re.compile(r'\d+.\d+.\d+.\d+:\d+')  #117.149.219.176:8123
    with open(proxy_file, 'r') as file_this:
        final_list = [line.strip() for line in file_this if pattern.match(line)]
    return final_list

#----------------------------------------------------------------------
def usage():
    """"""
    print('''Use as:
    -c: cid, room number
    -t: thread number
    -p: proxy file
    
    Press Ctrl+C to exit.
    ''')

if __name__=='__main__':
    is_proxy = False
    argv_list = sys.argv[1:]
    try:
        opts, args = getopt.getopt(argv_list, "hc:t:p:",
                                   ['help', "cid=", 'thread_number=', 'proxy_file='])
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
        if o in ('-p', '--proxy_file'):
            is_proxy = True
            proxy_file = a
    if is_proxy:
        proxy_list = proxy_file_to_list(proxy_file)
    print('Getting room {cid} {thread_number} viewers...'.format(cid = cid, thread_number = thread_number))
    main(cid, thread_number, is_proxy)
{% endhighlight %}

嘛，开包即用，效果良好。大家可以在[这里](/script/live_number.py)或者 [Github](https://gist.github.com/cnbeining/6b2273d7e332f29193d0) 上找到源码。

##用法

{% highlight bash %}
~ $ python live_number.py -c 12450 -t 500

-h 得到帮助  
-c 房间号（放肆！）  
-t 增加的人数  
-p 代理文件（以ip:port形式存储）
{% endhighlight %}

对了，你还需要`pip install websocket-client`一下

***

就是这样，点开导航栏中的 *cnBeining* 页面，你会发现更多有趣的东西~
