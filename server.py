from twisted.internet.protocol import Factory, Protocol
from twisted.internet import reactor
from GameState import GameState
import pickle

# this represents a connection between a client and the server
# two of these should exist
class GameConnection(Protocol):
	playerNumber = 0
	def __init__(self, dataDict):
		self.sharedData = dataDict

	def sendGameState(self):
		data = {'GAME_STATE' : self.sharedData['currentGameState'], 'GAME_STAGE' : self.sharedData['currentGameStage']}
		encodedData = pickle.dumps(data)
		self.sendData(encodedData)
	def connectionMade(self):
		self.sendGameState()

	def dataReceived(self, data):
		decodedData = pickle.loads(data)
		self.processRequest(decodedData)

	def sendData(self, data):
		self.transport.write(data)

	def processRequest(self, request):
		response = dict()
		if request['REQUEST_TYPE'] == 'PLAYER_CHOICE' and self.sharedData['currentGameStage']:
			response = self.processPlayerChoice(request)
		encodedResponse = pickle.dumps(response)
		self.sendData(encodedResponse)

	def processPlayerChoice(self, request):
		response = dict()
		playerChoice = request['PLAYER_CHOICE']
		if (playerChoice == 'KATARA' and self.sharedData['kataraPlayer'] != 0) or (playerChoice == 'AANG' and self.sharedData['aangPlayer'] != 0):
			response['RESPONSE'] = 'ERROR'
			response['REASON'] = 'Player already taken'
		elif playerChoice == 'KATARA':
			self.sharedData['kataraPlayer'] = self.playerNumber
			response['RESPONSE'] = 'SUCCESS'
			response['REASON'] = 'You are Katara'
		elif playerChoice == 'AANG':
			self.sharedData['aangPlayer']= self.playerNumber
			response['RESPONSE'] = 'SUCCESS'
			response['REASON'] = 'You are Aang'
		else:
			response['RESPONSE'] = 'ERROR'
			response['REASON'] = 'Player not found'
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
sharedData.update({'currentGameState' : GameState(), 'currentGameStage' : 'PLAYER_CHOICE', 'kataraPlayer' : 0, 'aangPlayer' : 0, "currentChatFactory" : ChatConnectionFactory(sharedData), "currentGameFactory" : GameConnectionFactory(sharedData)})

# connection to work
reactor.listenTCP(2580, sharedData["currentGameFactory"])
reactor.run()