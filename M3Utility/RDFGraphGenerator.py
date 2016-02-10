from M3Core.m3_kp import *
import random
import sys

def convert(triples):
    tl = []
    for t in triples:
        tr, stype, otype = t
        _s, _p, _o = tr
        if stype.lower() == "uri":
            s = URI(_s)
        elif stype.lower() == "literal":
            s = Literal(_s)
        else:
            s = bNode(_s)
        p = URI(_p)
        if otype.lower() == "uri":
            o = URI(_o)
        else:
            o = Literal(_o)
        tl.append(Triple(s, p, o))
    return tl


class PieceOfRDFGraph:
    
    def __init__(self,className,instanceName,attributeName):
        self.__className=className
        self.__instanceName=instanceName
        self.__attributeName=attributeName

    def getClassName(self):
        return self.__className

    def getInstanceName(self):
        return self.__instanceName

    def getAttributeName(self):
        return self.__attributeName


class RDFGraphGenerator:

    def __init__(self,pieces,numberOfInstances,numberOfAttributes):
        self.__pieces=pieces
        self.__numberOfInstances=numberOfInstances
        self.__numberOfAttributes=numberOfAttributes

        self.__minimumAttributeValueSize=0
        self.__minimumClassNamespaceSize=0
        self.__minimumInstanceNamespaceSize=0
        self.__minimumAttributeNamespaceSize=0

        self.__classNamespace=""
        self.__instanceNamespace=""
        self.__attributeNamespace=""
        self.__attributeValuePrefix=""

    def getPieces(self):
        return self.__pieces

    def getPiece(self,index):
        return self.__pieces[index]

    def getNumberOfInstance(self):
        return self.__numberOfInstances

    def getNumberOfAttributes(self):
        return self.__numberOfAttributes

    def setMinimumAttributeValueSize(self,size):
        self.__minimumAttributeValueSize=size
        self.__setAttributeValuePrefix()

    def setMinimumClassNamespaceSize(self,size):
        self.__minimumClassNamespaceSize=size
        self.__setClassNamespace()

    def setMinimumInstanceNamespaceSize(self,size):
        self.__minimumInstanceNamespaceSize=size
        self.__setInstanceNamespace()

    def setMinimumAttributeNamespaceSize(self,size):
        self.__minimumAttributeNamespaceSize=size
        self.__setAttributeNamespace()

    def getMinimumAttributeValueSize(self):
        return self.__minimumAttributeValueSize

    def getMinimumClassNamespaceSize(self):
        return self.__minimumClassNamespaceSize

    def getMinimumInstanceNamespaceSize(self):
        return self.__minimumInstanceNamespaceSize

    def getMinimumAttributeNamespaceSize(self):
        return self.__minimumAttributeNamespaceSize

    def __setClassNamespace(self):
        if self.getMinimumClassNamespaceSize()>0:
            for i in range(self.getMinimumClassNamespaceSize()):
                self.__classNamespace+="c"
            self.__classNamespace+="#"

    def __setInstanceNamespace(self):
        if self.getMinimumInstanceNamespaceSize()>0:
            for i in range(self.getMinimumInstanceNamespaceSize()):
                self.__instanceNamespace+="i"
            self.__instanceNamespace+="#"

    def __setAttributeNamespace(self):
        if self.getMinimumAttributeNamespaceSize()>0:
            for i in range(self.getMinimumAttributeNamespaceSize()):
                self.__attributeNamespace+="a"
            self.__attributeNamespace+="#"

    def __setAttributeValuePrefix(self):
        if self.getMinimumAttributeValueSize()>0:
            for i in range(self.getMinimumAttributeValueSize()):
                self.__attributeValuePrefix+="v"
            self.__attributeValuePrefix+="#"

    def getClassNamespace(self):
        return self.__classNamespace

    def getInstanceNamespace(self):
        return self.__instanceNamespace

    def getAttributeNamespace(self):
        return self.__attributeNamespace

    def getAttributeValuePrefix(self):
        return self.__attributeValuePrefix

    def createRDFGraph(self,node,ss_handle):
        insert = node.CreateInsertTransaction(ss_handle)
        class_namespace=self.getClassNamespace()
        instance_namespace=self.getInstanceNamespace()
        attribute_namespace=self.getAttributeNamespace()
        attribute_value_prefix=self.getAttributeValuePrefix()

        for index,i in enumerate(self.getPieces()):

            subject=class_namespace+i.getClassName()
            predicate="rdfs:subClassOf"
            object="thing"
            _triple=[((subject,predicate,object), "uri", "uri")]
            triple = convert(_triple)

        try:
            insert.send(triple, confirm = True)
        except M3Exception:
            print("Insert (init triples) failed:", M3Exception)

        for j in range(self.getNumberOfInstance()):

            subject=instance_namespace+i.getInstanceName()+str(j)
            predicate="rdf:type"
            object=class_namespace+i.getClassName()

            _triple=[((subject,predicate,object), "uri", "uri")]
            triple = convert(_triple)

        try:
            insert.send(triple, confirm = True)
        except M3Exception:
            print("Insert (init triples) failed:", M3Exception)

        for k in range(self.getNumberOfAttributes()):

            subject=instance_namespace+i.getInstanceName()+str(j)
            predicate=attribute_namespace+i.getAttributeName()+str(k)
            object="Value#"+attribute_value_prefix+str(hash(random.random())**2)

            _triple=[((subject,predicate,object), "uri", "literal")]
            triple = convert(_triple)

        try:
            insert.send(triple, confirm = True)
        except M3Exception:
            print("Insert (init triples) failed:", M3Exception)


        #print("Numero di triple inserite:" + str(3+len(self.getPieces())*(1+2*self.getNumberOfInstance()+self.getNumberOfInstance()*self.getNumberOfAttributes()+self.getNumberOfAttributes()+3))_
        node.CloseInsertTransaction(insert)



