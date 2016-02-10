from RDFGraphGenerator import *
from M3Core.m3_kp import *
from time import sleep
import time
import os


class SubscriptionsTest():
   
	def __init__(self,node,ss_handle):
		self.subscriptionsNumber=1
		self.RDFGraph=""
		self.node=node
		self.theSmartSpace=ss_handle
		self.step=1
		self.media=100
		self.triple=[]

	def setSubscriptionsNumber(self, number):
		self.subscriptionsNumber=number

	def setRDFGraph(self,graph):
		self.RDFGraph=graph

	def setStep(self,number):
		self.step=number

	def setMedia(self,number):
		self.media=number

	def getSubscriptionsNumber(self):
		return self.subscriptionsNumber

	def getRDFGraph(self):
		return self.RDFGraph

	def getStep(self):
		return self.step

	def getMedia(self):
		return self.media

	def setTriple(self,number):
		'''
		self._triple=[]
		for index in range(number):
			ins_triple=(URI("SSSSSSSSSSSSSSSSSSSS"+str(index)),URI("PPPPPPPPPPPPPPPPPPPP"+str(index)),URI("OOOOOOOOOOOOOOOOOOOO"+str(index)))
			#ins_triple=(URI("S"+str(index)),URI("P"+str(index)),URI("O"+str(index)))
			self.triple.append(ins_triple)	
		return self.triple
		'''

		counter=0
		if number>0:
			for piece in self.RDFGraph.getPieces():
				for i in range(self.RDFGraph.getNumberOfInstance()):
					for k in range(self.RDFGraph.getNumberOfAttributes()):
						subject= self.RDFGraph.getInstanceNamespace()+piece.getInstanceName()+str(i)
						predicate=self.RDFGraph.getAttributeNamespace()+piece.getAttributeName()+str(k)
						ins_triple=(URI(subject),URI(predicate),Literal("OOOOOOOOOOOOOOOOOOOO"+str(counter)))
						self.triple.append(ins_triple)
						counter+=1
						if counter>=number:
							break
					if counter>=number:
						break
				if counter>=number:
					break
			if counter<number:
				print("Servono altre sottoscrizioni - Aumentare il numero delle istanze")

		print("ins list :" +str(self.triple))

	def getTriple(self):
		return self.triple

	def runTest(self,test):
		self.subscriptionID=[]
		self.subscriptionList=[]
		self.result=[]
		output = open("./data.txt","w")
		# creo la lista di triple da sottoscrivere (sono quelle generate da RDFGraphGenerator)
		counter=0
		if self.subscriptionsNumber>0:
			for piece in self.RDFGraph.getPieces():
				for i in range(self.RDFGraph.getNumberOfInstance()):
					for k in range(self.RDFGraph.getNumberOfAttributes()):
						subject= self.RDFGraph.getInstanceNamespace()+piece.getInstanceName()+str(i)
						predicate=self.RDFGraph.getAttributeNamespace()+piece.getAttributeName()+str(k)
						ins_triple=(URI(subject),URI(predicate),URI("http://www.nokia.com/NRC/M3/sib#any"))
						self.subscriptionList.append(ins_triple)
						counter+=1
						if counter>=self.subscriptionsNumber:
							break
					if counter>=self.subscriptionsNumber:
						break
				if counter>=self.subscriptionsNumber:
					break
			if counter<self.subscriptionsNumber:
				print "Servono altre sottoscrizioni - Aumentare il numero delle istanze"


		

		# avvio il test 
		counter=0
		while counter <= self.subscriptionsNumber:
			print "\nwaiting for start test whit",counter,"subscriptions..."
			sleep(1)
			time = self.__runTest(test,self.node,self.theSmartSpace,self.media,self.triple)
			self.result.append(time)
			print test+"--> "+str(time)
			print "performance test ok" 
			output.write(str(counter)+"\t"+str(time)+"\n")

			if counter + self.step > self.subscriptionsNumber:
				break

			for k in range(self.step):
				self.rs = self.node.CreateSubscribeTransaction(self.theSmartSpace)
				self.subscriptionID.append(self.rs)
				self.rs.subscribe_rdf(self.subscriptionList[counter], RdfMsgHandler())		
				#print "added : " + str(self.subscriptionList[counter])
				counter+=1

		output.close()
		print "\n*** Test result ***"
		k=len(self.result)
		for i in range(k):
			print "subscription open:",i*self.step,"\ttime:",self.result[i]


	def __runTest(self,test,node,ss_handle,repetitions,triple):
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


	def closeSubscriptions(self):
		for subscription in self.subscriptionID:
			self.node.CloseSubscribeTransaction(subscription)
			print "close subscription: ",subscription



class RdfMsgHandler:

	def handle(self, added, removed):
		'''
		print "RDF Subscription notification:"
		for i in added:
			print "Added:", str(i)
		for i in removed:
			print "Removed:", str(i)
		'''
