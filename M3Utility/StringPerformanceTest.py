from Utility import SmartSpaceData
from RDFGraphGenerator import *
from M3Core.m3_kp import *
from time import sleep
import time
import os


class StringTest():
   
	def __init__(self,node,ss_handle):
		self.protectionsNumber=1
		self.subscriptionsNumber=1
		self.node = node
		self.theSmartSpace = ss_handle
		self.media=100
		self.triple=[]


	def setMedia(self,number):
		self.media=number

	def setTriple(self,number):
		self.triple=[]
		S="#"
		P="#"
		O="#"		
		for index in range(number):
			S=S+"S"
			P=P+"P"
			O=O+"O"
		self.triple=(URI(S),URI(P),URI(O))
		return self.triple

	def runTest(self,uri):
		self.result=[]
		counter=0
		while counter <= uri:
			print "\nwaiting for start test whit uri lenght:",counter
			triple = self.setTriple(counter)			
			#print triple			
			sleep(1)
			time = self.__runTest(self.node,self.theSmartSpace,self.media,self.triple)
			self.result.append(time)
			counter+=500
			print "insert--> "+str(time)
			print "performance test ok" 			
	
		print "\n*** Test result ***"
		k=len(self.result)
		for i in range(k):
			print "lunghezza uri:",i,"\ttime:",self.result[i]


	def __runTest(self,node,ss_handle,repetitions,triple):
		elapsedTime=[]
		for index in range(repetitions):
			qs=node.CreateInsertTransaction(ss_handle)
			start=time.time()
			qs.send(triple, confirm = True)
			elapsedTime.append(time.time()-start)
			node.CloseInsertTransaction(qs)

			qs=node.CreateRemoveTransaction(ss_handle)
			qs.remove(triple, confirm = True)
			node.CloseRemoveTransaction(qs)
		
		return sum(elapsedTime)/len(elapsedTime)	




