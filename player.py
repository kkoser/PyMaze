from twisted.internet.protocol import Factory, ClientFactory, Protocol
from twisted.internet import reactor, stdio
import pickle
from twisted.internet.task import LoopingCall
from game import GameSpace
from twisted.protocols.basic import LineReceiver
import pprint
import sys

class ServerConnection(Protocol):
	def __init__(self, dataDict):
		self.sharedData = dataDict

	def dataReceived(self, data):
		decodedData = pickle.loads(data)
		self.processResponse(decodedData)

	def connectionMade(self):
		# save connection for callback
		self.sharedData['gameSpace'].connection = self
		self.askForMenuState()

	def sendData(self, data):
		encodedData = pickle.dumps(data)
		self.transport.write(encodedData)

	def processResponse(self, response):
		if response['RESPONSE_TYPE'] == 'GAME_STATE':
			self.sharedData['gameSpace'].activeScreen.state = response['RESPONSE_DATA']
			self.sharedData['gameSpace'].playerNumber = response['PLAYER_NUMBER']
		elif response['RESPONSE_TYPE'] == 'MENU_STATE_RESPONSE':
			self.sharedData['gameSpace'].activeScreen = self.sharedData['gameSpace'].mainMenuScreen
			# update game state
			self.sharedData['gameSpace'].activeScreen.state = response['RESPONSE_DATA']
			self.sharedData['gameSpace'].playerNumber = response['PLAYER_NUMBER']

			#check for transition to game screen
			if response['RESPONSE_DATA'].aangPlayerReady and response['RESPONSE_DATA'].kataraPlayerReady:
				# get game state
				self.askForInitialGameState()

		elif response['RESPONSE_TYPE'] == 'GAME_STATE_RESPONSE':
			self.sharedData['gameSpace'].activeScreen = self.sharedData['gameSpace'].gameScreen

			# update game state
			self.sharedData['latestGameState'] = response['RESPONSE_DATA']
			self.sharedData['gameSpace'].activeScreen.state = response['RESPONSE_DATA']
			self.sharedData['gameSpace'].playerNumber = response['PLAYER_NUMBER']

	def sendMenuState(self, menuState):
		request = {'REQUEST_TYPE' : 'MENU_STATE_UPDATE_REQUEST', 'REQUEST_DATA' : menuState}
		self.sendData(request)

	def sendGameState(self, gameState):
		request = {'REQUEST_TYPE' : 'GAME_STATE_UPDATE_REQUEST', 'REQUEST_DATA' : gameState}
		self.sendData(request)

	def askForGameState(self):
		request = {'REQUEST_TYPE' : 'GAME_STATE_REQUEST'}
		self.sendData(request)

	def askForMenuState(self):
		request = {'REQUEST_TYPE' : 'MENU_STATE_REQUEST'}
		self.sendData(request)

	def askForInitialGameState(self):
		request = {'REQUEST_TYPE' : 'GAME_STATE_INITIAL_REQUEST'}
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

class ChatConnection(LineReceiver):

	def __init__(self, dataDict):
		self.sharedData = dataDict

	def lineReceived(self, line):
		print "From your lover:", line
		sys.stdout.write(">>> ") # no newline
		sys.stdout.flush()


class ChatConnectionFactory(Factory):
	currentConnection = None

	def __init__(self, dataDict):
		self.sharedData = dataDict

	def buildProtocol(self, addr):
		self.currentConnection = ChatConnection(self.sharedData)
		return self.currentConnection

	def startedConnecting(self, connector):
		pass

	def clientConnectionLost(self, connector, reason):
		print 'Lost connection.  Reason:', reason

	def clientConnectionFailed(self, connector, reason):
		print 'Connection failed. Reason:', reason

class Echo(LineReceiver):
	from os import linesep as delimiter

	def __init__(self, dataDict):
		self.sharedData = dataDict

	def connectionMade(self):
		self.transport.write('>>> ')

	def lineReceived(self, line):
		if self.sharedData['currentChatFactory'] is not None:
			pass
			self.sharedData['currentChatFactory'].currentConnection.sendLine(line)
		else:
			self.transport.write("Error: you are not connected")
		self.transport.write('>>> ')

if __name__ == '__main__':

	sharedData = dict()
	sharedData.update({'currentChatFactory' : ChatConnectionFactory(sharedData), "currentServerFactory" : ServerConnectionFactory(sharedData), 'gameSpace' : GameSpace()})

	# set up pygame loop
	sharedData['gameSpace'].main()
	lc = LoopingCall(sharedData['gameSpace'].tick)
	lc.start(1.0/30.0)

	reactor.connectTCP("localhost", 2580, sharedData['currentServerFactory'])
	reactor.connectTCP("localhost", 2581, sharedData['currentChatFactory'])
	stdio.StandardIO(Echo(sharedData))

	reactor.run()