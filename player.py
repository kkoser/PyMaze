from twisted.internet.protocol import Factory, ClientFactory, Protocol
from twisted.internet import reactor
import pickle
from twisted.internet.task import LoopingCall
from game import GameSpace

class ServerConnection(Protocol):
	def __init__(self, dataDict):
		self.sharedData = dataDict

	def dataReceived(self, data):
		print data
	def connectionMade(self):
		request = {'REQUEST_TYPE' : 'PLAYER_CHOICE', 'PLAYER_CHOICE' : 'KATARA'}
		encodedRequest = pickle.dumps(request)
		self.sendData(encodedRequest)
	def sendData(self, data):
		self.transport.write(data)

class ServerConnectionFactory(ClientFactory):
	currentConnection = None

	def __init__(self, dataDict):
		self.sharedData = dataDict

	def startedConnecting(self, connector):
		pass

	def buildProtocol(self, addr):
		self.currentConnection = ServerConnection(self.sharedData)
		return self.currentConnection

	def clientConnectionLost(self, connector, reason):
		print 'Lost connection.  Reason:', reason

	def clientConnectionFailed(self, connector, reason):
		print 'Connection failed. Reason:', reason

if __name__ == '__main__':

	sharedData = dict()
	sharedData.update({"currentServerFactory" : ServerConnectionFactory(sharedData)})

	# set up pygame loop
	gs = GameSpace()
	gs.main()
	lc = LoopingCall(gs.tick)
	lc.start(1.0/30.0)


	host = "localhost"
	port = 2580
	reactor.connectTCP(host, port, sharedData['currentServerFactory'])
	reactor.run()