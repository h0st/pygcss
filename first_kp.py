#!/usr/bin/python
# -*- coding: utf-8 -*-

from M3Core.m3_kp import *
import uuid

# Simple class for join/leave smart space
#
class FirstKP(KP):
	def __init__(self, server_ip, server_port):
		KP.__init__(self, str(uuid.uuid4())+"_FirstKP")
		self.ss_handle = ("X", (TCPConnector, (server_ip,server_port)))

	def join_sib(self):
		self.join(self.ss_handle)
		print "Joined"
	
	def leave_sib(self):
		self.leave(self.ss_handle)
		print "Leave"

pd = FirstKP("127.0.0.1", 10010)
pd.join_sib()
pd.leave_sib()
