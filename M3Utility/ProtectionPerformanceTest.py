from M3Utility.Utility import SmartSpaceData
from M3Core.m3_kp import *
from time import sleep
import time
import os


class ProtectionsTest():
   
	def __init__(self,node,ss_handle):
		self.protectionsNumber=1
		self.node = node
		self.theSmartSpace = ss_handle
		self.step=1
		self.media=100
		self.triple=[]

	def setProtectionsNumber(self, number):
		self.protectionsNumber=number

	def setStep(self,number):
		self.step=number

	def setMedia(self,number):
		self.media=number

	def getProtectionsNumber(self):
		return self.protectionsNumber

	def getStep(self):
		return self.step

	def getMedia(self):
		return self.media

	def setTriple(self,number):
		self._triple=[]
		for index in range(number):
			ins_triple=(URI("SSSSSSSSSSSSSSSSSSSS"+str(index)),URI("PPPPPPPPPPPPPPPPPPPP"+str(index)),URI("OOOOOOOOOOOOOOOOOOOO"+str(index)))
			#ins_triple=(URI("S"+str(index)),URI("P"+str(index)),URI("O"+str(index)))			
			self.triple.append(ins_triple)
		print self.triple
		return self.triple

	def getTriple(self):
		return self.triple

	def runTest(self,test,kp):
		self.result=[]
		self.protectionsList=[]
		output = open("./data.txt","w") 
		counter=0
		while counter <= self.protectionsNumber:
			print "\nwaiting for start test whit",counter,"protections..."
			sleep(5)
			if kp == 1:
				time = self.__runTest1KP(test,self.node,self.theSmartSpace,self.media,self.triple)			
			if kp == 2:
				time = self.__runTest2KP(test,self.media,self.triple)
			self.result.append(time)
			print test+"--> "+str(time)
			print "performance test ok" 
			output.write(str(counter)+"\t"+str(time)+"\n")

			if counter + self.step > self.protectionsNumber:
				break

			for k in range(self.step):
				subject="S#"+str(counter)
				predicate=["P#"+str(counter)]
				status = self.node.InsertProtection(subject,predicate,self.theSmartSpace)
				insert=(subject,predicate)
				self.protectionsList.append(insert)
				counter+=1

		output.close()
		print "\n*** Test result ***"
		k=len(self.result)
		for i in range(k):
			print "protection open:",i*self.step,"\ttime:",self.result[i]


	def __runTest1KP(self,test,node,ss_handle,repetitions,triple):
		elapsedTime=[]
		if test == "insert":
			for index in range(repetitions):
				qs=node.CreateInsertTransaction(ss_handle)
				start=time.time()
				qs.send(triple, confirm = True)
				elapsedTime.append(time.time()-start)
				node.CloseInsertTransaction(qs)

				qs=node.CreateRemoveTransaction(ss_handle)
				qs.remove(triple, confirm = True)
				node.CloseRemoveTransaction(qs)
		if test == "remove":
			for index in range(repetitions):
				qs=node.CreateInsertTransaction(ss_handle)
				qs.send(triple, confirm = True)
				node.CloseInsertTransaction(qs)

				qs=node.CreateRemoveTransaction(ss_handle)
				start=time.time()
				qs.remove(triple, confirm = True)
				elapsedTime.append(time.time()-start)
				node.CloseRemoveTransaction(qs)

		return sum(elapsedTime)/len(elapsedTime)


	def __runTest2KP(self,test,repetitions,triple):
		# connessione automatica
		smartSpace=SmartSpaceData()
		smartSpace.setSmartSpaceName("X")
		smartSpace.setIPADDR("localhost")
		smartSpace.setPort(10010)

		if not smartSpace.joinSpace():
			sys.exit('Could not join to Smart Space')

		node=smartSpace.getNode()
		ss_handle = smartSpace.getSmartSpace()

		elapsedTime=[]
		if test == "insert":
			for index in range(repetitions):
				qs=node.CreateInsertTransaction(ss_handle)
				start=time.time()
				qs.send(triple, confirm = True)
				elapsedTime.append(time.time()-start)
				node.CloseInsertTransaction(qs)

				qs=node.CreateRemoveTransaction(ss_handle)
				qs.remove(triple, confirm = True)
				node.CloseRemoveTransaction(qs)
		if test == "remove":
			for index in range(repetitions):
				qs=node.CreateInsertTransaction(ss_handle)
				qs.send(triple, confirm = True)
				node.CloseInsertTransaction(qs)

				qs=node.CreateRemoveTransaction(ss_handle)
				start=time.time()
				qs.remove(triple, confirm = True)
				elapsedTime.append(time.time()-start)
				node.CloseRemoveTransaction(qs)
		smartSpace.leaveSpace()
		return sum(elapsedTime)/len(elapsedTime)
		


	def closeProtections(self):
		print "Chiudo le protezioni..."
		for subject, predicate in self.protectionsList:
			self.node.RemoveProtection(subject,predicate,self.theSmartSpace)
		print "Protezioni chiuse!"


