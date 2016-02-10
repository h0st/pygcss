from M3Core.m3_kp import *

class SmartSpaceData:
   
    def __init__(self):
        self.SmartSpaceName = " "
        self.IPADDR = "127.0.0.1"
        self.Port = 10010
        self.nodename = str(uuid.uuid4())
        self.theNode = KP(self.nodename)
        self.theSmartSpace = ""

    def setParameters(self,n,i,p):
        self.SmartSpaceName = n
        self.IPADDR = i
        self.Port = p

    def getSmartSpaceName(self):
        return self.SmartSpaceName

    def getIPADDR(self):
        return self.IPADDR

    def getNodeName(self):
        return self.nodename

    def getPort(self):
        return self.Port

    def getNode(self):
        print(self.theNode)
        return self.theNode

    def getSmartSpace(self):
        return self.theSmartSpace

    def setSmartSpaceName(self,n):
        self.SmartSpaceName = str(n)

    def setIPADDR(self,i):
        self.IPADDR = str(i)

    def setPort(self,p):
        self.Port = int(p)

    def joinSpace(self):
        self.theSmartSpace = ( self.SmartSpaceName, (TCPConnector, (self.IPADDR,self.Port)  ))
        ans = self.theNode.join(self.theSmartSpace)
        return ans

    def leaveSpace(self):
        ans = self.theNode.leave(self.theSmartSpace)
        return ans
