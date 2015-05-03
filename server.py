from twisted.internet.protocol import Factory, Protocol
from twisted.internet import reactor
from GameState import GameState
import pickle
from MenuState import MenuState

# possible screens: MENU_SCREEN, GAME_SCREEN
# possible requests: GAME_STATE_REQUEST, PLAYER_CHOICE_REQUEST, GAME_STATE_UPDATE_REQUEST

# this represents a connection between a client and the server
# two of these should exist
class GameConnection(Protocol):
	playerNumber = 0
	def __init__(self, dataDict):
		self.sharedData = dataDict

	def getCurrentState(self):
		data = {'RESPONSE_TYPE' : 'GAME_STATE_RESPONSE', 'CURRENT_SCREEN' : self.sharedData['currentGameScreen']}
		if self.sharedData['currentGameScreen'] == 'MENU_SCREEN':
			data['RESPONSE_DATA'] = self.sharedData['currentMenuState']
		else:
			data['RESPONSE_DATA'] = self.sharedData['currentGameState']
		return data

	def connectionMade(self):
		self.sendData(self.getCurrentState())

	def dataReceived(self, data):
		decodedData = pickle.loads(data)
		self.respondToRequest(decodedData)

	def sendData(self, data):
		encodedData = pickle.dumps(data)
		self.transport.write(encodedData)

	def respondToRequest(self, request):
		response = dict()
		if request['REQUEST_TYPE'] == 'GAME_STATE_REQUEST':
			response = self.getCurrentState()
		elif request['REQUEST_TYPE'] == 'PLAYER_CHOICE_REQUEST' and self.sharedData['currentGameScreen'] == 'MENU_SCREEN':
			response = self.processPlayerChoice(request)
		self.sendData(response)

	def processPlayerChoice(self, request):
		response = dict()
		playerChoice = request['PLAYER_CHOICE']
		if (playerChoice == 'KATARA' and self.sharedData['currentMenuState'].kataraPlayer != 0) or (playerChoice == 'AANG' and self.sharedData['currentMenuState'].aangPlayer != 0):
			response['RESPONSE'] = 'ERROR'
			response['REASON'] = 'Player already taken'
		elif playerChoice == 'KATARA':
			self.sharedData['currentMenuState'].kataraPlayer = self.playerNumber
			response['RESPONSE'] = 'SUCCESS'
			response['REASON'] = 'You are Katara'
		elif playerChoice == 'AANG':
			self.sharedData['currentMenuState'].aangPlayer = self.playerNumber
			response['RESPONSE'] = 'SUCCESS'
			response['REASON'] = 'You are Aang'
		else:
			response['RESPONSE'] = 'ERROR'
			response['REASON'] = 'Player not found'

		response['MENU_STATE'] = self.sharedData['currentMenuState']
		return response


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