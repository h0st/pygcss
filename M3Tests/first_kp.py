#!/usr/bin/python
# -*- coding: utf-8 -*-

from M3Core.m3_kp import *  # import sm2
import uuid


# Simple class for join/leave smart space
#
class FirstKP(KP):
	def __init__(self, server_ip, server_port):
		self.kp_name = str(uuid.uuid4())+"_FirstKP"
		KP.__init__(self, self.kp_name)
		self.ss_handle = ("X", (TCPConnector, (server_ip, server_port)))

	def join_sib(self):
		self.join(self.ss_handle)
		print "Joined "+self.kp_name
	
	def leave_sib(self):
		self.leave(self.ss_handle)
		print "Leave "+self.kp_name


pd = FirstKP("127.0.0.1", 10010)
pd.join_sib()
pd.leave_sib()
