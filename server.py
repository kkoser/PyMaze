from twisted.internet.protocol import Factory, Protocol
from twisted.internet import reactor
from GameState import GameState
import pickle
from MenuState import MenuState

# possible screens: MENU_SCREEN, GAME_SCREEN
# possible requests: GAME_STATE_REQUEST, PLAYER_CHOICE_REQUEST, GAME_STATE_UPDATE_REQUEST, MENU_STATE_UPDATE_REQUEST

# this represents a connection between a client and the server
# two of these should exist
class GameConnection(Protocol):
	playerNumber = 0
	def __init__(self, dataDict):
		self.sharedData = dataDict

	def connectionMade(self):
		pass

	def dataReceived(self, data):
		decodedData = pickle.loads(data)
		self.respondToRequest(decodedData)

	def sendData(self, data):
		encodedData = pickle.dumps(data)
		self.transport.write(encodedData)

	def respondToRequest(self, request):
		response = dict()
		if request['REQUEST_TYPE'] == 'MENU_STATE_UPDATE_REQUEST':
			self.sharedData['currentMenuState'] = request['REQUEST_DATA']
			data = {'RESPONSE_TYPE' : 'MENU_STATE_RESPONSE', 'PLAYER_NUMBER' : self.playerNumber, 'RESPONSE_DATA' : self.sharedData['currentMenuState']}
			self.sendDataToBothPlayers(data)
		elif request['REQUEST_TYPE'] == 'GAME_STATE_UPDATE_REQUEST':
			self.sharedData['currentGameState'] = request['REQUEST_DATA']
			data = {'RESPONSE_TYPE' : 'GAME_STATE_RESPONSE', 'PLAYER_NUMBER' : self.playerNumber, 'RESPONSE_DATA' : self.sharedData['currentGameState']}
			self.sendDataToBothPlayers(data)
		elif request['REQUEST_TYPE'] == 'MENU_STATE_REQUEST':
			data = {'RESPONSE_TYPE' : 'MENU_STATE_RESPONSE', 'PLAYER_NUMBER' : self.playerNumber, 'RESPONSE_DATA' : self.sharedData['currentMenuState']}
			self.sendData(data)
		elif request['REQUEST_TYPE'] == 'GAME_STATE_REQUEST':
			data = {'RESPONSE_TYPE' : 'GAME_STATE_RESPONSE', 'PLAYER_NUMBER' : self.playerNumber, 'RESPONSE_DATA' : self.sharedData['currentGameState']}
			self.sendData(data)

	def sendDataToBothPlayers(self, data):
		#send it to both players if they're online
		if self.sharedData['currentGameFactory'].player1Connection is not None:
			data['PLAYER_NUMBER'] = 1
			self.sharedData['currentGameFactory'].player1Connection.sendData(data)
		if self.sharedData['currentGameFactory'].player2Connection is not None:
			data['PLAYER_NUMBER'] = 2
			self.sharedData['currentGameFactory'].player2Connection.sendData(data)

class GameConnectionFactory(Factory):
	player1Connection = None
	player2Connection = None

	def __init__(self, dataDict):
		self.sharedData = dataDict

	def buildProtocol(self, addr):
		# determine who is player1
		if self.player1Connection is None:
			self.player1Connection = GameConnection(self.sharedData)
			self.player1Connection.playerNumber = 1
			return self.player1Connection
		else:
			self.player2Connection = GameConnection(self.sharedData)
			self.player2Connection.playerNumber = 2
			return self.player2Connection

class ChatConnection(Protocol):

	def __init__(self, dataDict):
		self.sharedData = dataDict

	def connectionMade(self):
		# listen for data connection
		reactor.listenTCP(2581, sharedData["currentDataFactory"])
		# ask for data connection
		self.sharedData['currentGameFactory'].currentConnection.sendData("REQUESTING_DATA_CONNECTION")
		# see if there is data that needs sending
		while (len(self.sharedData['toSSHQueue'].waiting) > 0):
			d = self.sharedData['toSSHQueue'].get()
			d.addCallback(self.sendData)

	def connectionLost(self, reason):
		print("connection lost", reason)

	def dataReceived(self, data):
		# pass on the data
		if self.sharedData['currentDataFactory'].currentConnection is not None:
			self.sharedData['currentDataFactory'].currentConnection.sendData(data)
		else:
			self.sharedData['toDataQueue'].put(data)

	def sendData(self, data):
		self.transport.write(data)

class ChatConnectionFactory(Factory):
	currentConnection = None

	def __init__(self, dataDict):
		self.sharedData = dataDict

	def buildProtocol(self, addr):
		self.currentConnection = SSHConnection(self.sharedData)
		return self.currentConnection



sharedData = dict()
#state refers to data pertaining to the game
#screen refers to the point of the game
sharedData.update({'currentGameState' : GameState(), 'currentMenuState' : MenuState(), 'currentGameScreen' : 'MENU_SCREEN', "currentChatFactory" : ChatConnectionFactory(sharedData), "currentGameFactory" : GameConnectionFactory(sharedData)})

# connection to work
reactor.listenTCP(2580, sharedData["currentGameFactory"])
reactor.run()