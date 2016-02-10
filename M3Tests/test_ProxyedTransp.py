#!/usr/bin/env python

"""
Proxy class for XML-PRC
"""

__author__ = "Mezhenin Artoym <mezhenin@cs.karelia.ru>"
__version__ = "$Revision: 0.1 $"
__date__ = "$Date: 2010/01/10 $"
__copyright__ = ""
__license__ = "GPLv2"

import xmlrpclib
import httplib

class ProxyedTransp (xmlrpclib.Transport):
    """
    To access an XML-RPC server through a proxy, you need to define a 
    custom transport.
    This is example from the official documentation.
    http://docs.python.org/library/xmlrpclib.html
    """
    def set_proxy(self, proxy):
        """
        Actually I do not know what this funct. is for...
        """
        self.proxy = proxy

    def make_connection(self, host):
        """
         ... sorry guys ...
        """
        self.realhost = host
        return httplib.HTTP(self.proxy)

    def send_request(self, connection, handler, request_body):
        """
        ... I thought that the xml-rps should have its 
            own class for the proxy ...
        """
        connection.putrequest("POST", 'http://%s%s' % (self.realhost, handler))

    def send_host(self, connection, host):
        """
        ... but it is not :^(
        """
        #connection.putheader('Host', self.realhost) - officail doc
        connection.putheader(self.realhost)


