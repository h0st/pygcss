from M3Utility.RDFGraphGenerator import *
from M3Utility.SubscriptionPerformanceTest import *
from M3Utility.ProtectionPerformanceTest import *
from M3Utility.Utility import SmartSpaceData
from M3Utility.StringPerformanceTest import *
from time import sleep
from M3Core.m3_kp import *
import os

if __name__ == "__main__":
    while 1:
      
	# connessione automatica
	smartSpace=SmartSpaceData()
	smartSpace.setSmartSpaceName("X")
	smartSpace.setIPADDR("127.0.0.1")
	smartSpace.setPort(10010)

	if not smartSpace.joinSpace():
		sys.exit('Could not join to Smart Space')

	node=smartSpace.getNode()
	ss_handle = smartSpace.getSmartSpace()

	triple=(URI("sib:any"),URI("sib:any"),URI("sib:any"))
	qs=node.CreateRemoveTransaction(ss_handle)
	qs.remove(triple, confirm = True)
	node.CloseRemoveTransaction(qs)
	sleep(5)

	# creazione grafo
	pieces=[]
	pieces.append(PieceOfRDFGraph("ClasseA","IstanzaA","AttributoA"))
	pieces.append(PieceOfRDFGraph("ClasseB","IstanzaB","AttributoB"))
	pieces.append(PieceOfRDFGraph("ClasseC","IstanzaC","AttributoC"))
	pieces.append(PieceOfRDFGraph("ClasseD","IstanzaD","AttributoD"))
	pieces.append(PieceOfRDFGraph("ClasseE","IstanzaE","AttributoE"))
	pieces.append(PieceOfRDFGraph("ClasseF","IstanzaF","AttributoF"))
	pieces.append(PieceOfRDFGraph("ClasseG","IstanzaG","AttributoG"))
	pieces.append(PieceOfRDFGraph("ClasseH","IstanzaH","AttributoH"))
	pieces.append(PieceOfRDFGraph("ClasseI","IstanzaI","AttributoI"))
	pieces.append(PieceOfRDFGraph("ClasseJ","IstanzaJ","AttributoJ"))

	RDFGraph=RDFGraphGenerator(pieces,40,30)
	RDFGraph.setMinimumClassNamespaceSize(5)
	RDFGraph.setMinimumInstanceNamespaceSize(5)
	RDFGraph.setMinimumAttributeNamespaceSize(5)
	RDFGraph.setMinimumAttributeValueSize(5)

	## inserimento del grafo nella SIB (opzionale)
	RDFGraph.createRDFGraph(node,ss_handle)
	sleep(10)

	## subscription performance test ("insert" - "remove")
	
	SUBGen=SubscriptionsTest(node,ss_handle)
	SUBGen.setSubscriptionsNumber(10)
	SUBGen.setMedia(50)
	SUBGen.setStep(1)
	SUBGen.setTriple(1)
	SUBGen.setRDFGraph(RDFGraph)
	SUBGen.runTest("insert")
	SUBGen.closeSubscriptions()
		

	## protection performance test ("insert" - "remove")
	#PROTGen=ProtectionsTest(node,ss_handle)
	#PROTGen.setProtectionsNumber(10)
	#PROTGen.setMedia(10)
	#PROTGen.setStep(1)
	#PROTGen.setTriple(1)
	#PROTGen.runTest("insert",1)
	#PROTGen.closeProtections()

	## test lunghezza uri triple inserite
	#URITest=StringTest(node,ss_handle)
	#URITest.setMedia(10)
	#URITest.runTest(10000)


	smartSpace.leaveSpace()
	print "leave SIB..."




