from twisted.internet.protocol import Factory, ClientFactory, Protocol
from twisted.internet import reactor
import pickle
from twisted.internet.task import LoopingCall
from game import GameSpace

class ServerConnection(Protocol):
	def __init__(self, dataDict):
		self.sharedData = dataDict

	def dataReceived(self, data):
		decodedData = pickle.loads(data)
		self.processResponse(decodedData)

	def connectionMade(self):
		# save connection for callback
		self.sharedData['gameSpace'].connection = self
		# initial request
		self.askForGameState()

	def sendData(self, data):
		encodedData = pickle.dumps(data)
		self.transport.write(encodedData)

	def askForGameState(self):
		request = {'REQUEST_TYPE' : 'GAME_STATE_REQUEST'}
		self.sendData(request)

	def processResponse(self, response):
		if response['RESPONSE_TYPE'] == 'GAME_STATE_RESPONSE' or response['RESPONSE_TYPE'] == 'MENU_STATE_RESPONSE':
			# update game state
			print vars(response['RESPONSE_DATA'])
			self.sharedData['gameSpace'].activeScreen.state = response['RESPONSE_DATA']
			print response['PLAYER_NUMBER']
			self.sharedData['gameSpace'].playerNumber = response['PLAYER_NUMBER']

	def sendMenuState(self, menuState):
		request = {'REQUEST_TYPE' : 'MENU_STATE_UPDATE_REQUEST', 'REQUEST_DATA' : menuState}
		self.sendData(request)

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
	sharedData.update({"currentServerFactory" : ServerConnectionFactory(sharedData), 'gameSpace' : GameSpace()})

	# set up pygame loop
	sharedData['gameSpace'].main()
	lc = LoopingCall(sharedData['gameSpace'].tick)
	lc.start(1.0/30.0)


	host = "localhost"
	port = 2580
	reactor.connectTCP(host, port, sharedData['currentServerFactory'])
	reactor.run()