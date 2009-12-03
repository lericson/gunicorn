# -*- coding: utf-8 -*-
#
# Copyright 2008,2009 Benoit Chesneau <benoitc@e-engura.org>
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at#
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

import socket

class Socket(socket.socket):
    def accept_nonblock(self):
        conn, addr = self.accept()
        conn.setblocking(0)
        return (conn, addr)


class TCPServer(Socket):
    """class for server-side TCP sockets. 
    This is wrapper around socket.socket class"""
    
    def __init__(self, address, **opts):
        self.backlog = opts.get('backlog', 1024)
        self.timeout = opts.get('timeout', 300)
        self.reuseaddr = opts.get('reuseaddr', True)
        self.nodelay = opts.get('nodelay', True)
        
        socket.socket.__init__(self, socket.AF_INET, socket.SOCK_STREAM)

        self.bind(address)
        self.listen(self.backlog)
        
        # set options
        self.settimeout(self.timeout)
        self.setblocking(0)
        if self.reuseaddr:
            self.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
             
        if self.nodelay:
            self.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)