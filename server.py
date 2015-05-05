from twisted.internet.protocol import Factory, Protocol
from twisted.internet import reactor
from GameState import GameState
import pickle
from MenuState import MenuState
from twisted.protocols.basic import LineReceiver

# this represents a connection between a client and the server
# two of these should exist
class GameConnection(Protocol):
	playerNumber = 0 # for this specific connection
	def __init__(self, dataDict):
		self.sharedData = dataDict

	def connectionMade(self):
		pass

	def dataReceived(self, data):
		# decode and pass on 
		decodedData = pickle.loads(data)
		self.respondToRequest(decodedData)

	def sendData(self, data):
		# encode and pass on
		encodedData = pickle.dumps(data)
		self.transport.write(encodedData)

	def respondToRequest(self, request):
		# check the request type and then process
		if request['REQUEST_TYPE'] == 'MENU_STATE_UPDATE_REQUEST':
			self.sharedData['currentMenuState'] = request['REQUEST_DATA'] # update menu state
			data = {'RESPONSE_TYPE' : 'MENU_STATE_RESPONSE', 'PLAYER_NUMBER' : self.playerNumber, 'RESPONSE_DATA' : self.sharedData['currentMenuState']}
			self.sendDataToBothPlayers(data) # update both players with the new menu state
		elif request['REQUEST_TYPE'] == 'GAME_STATE_UPDATE_REQUEST':
			self.sharedData['currentGameState'] = request['REQUEST_DATA'] # update game state
			# change turn
			self.sharedData['currentGameState'].playerTurnNumber = self.sharedData['currentGameState'].playerTurnNumber % 2 + 1
			data = {'RESPONSE_TYPE' : 'GAME_STATE_RESPONSE', 'PLAYER_NUMBER' : self.playerNumber, 'RESPONSE_DATA' : self.sharedData['currentGameState']}
			self.sendDataToBothPlayers(data) # update both players with the new menu state
		elif request['REQUEST_TYPE'] == 'MENU_STATE_REQUEST': # just asking for state
			data = {'RESPONSE_TYPE' : 'MENU_STATE_RESPONSE', 'PLAYER_NUMBER' : self.playerNumber, 'RESPONSE_DATA' : self.sharedData['currentMenuState']}
			self.sendData(data) 
		elif request['REQUEST_TYPE'] == 'GAME_STATE_REQUEST': # just asking for state
			data = {'RESPONSE_TYPE' : 'GAME_STATE_RESPONSE', 'PLAYER_NUMBER' : self.playerNumber, 'RESPONSE_DATA' : self.sharedData['currentGameState']}
			self.sendData(data)
		elif request['REQUEST_TYPE'] == 'GAME_STATE_INITIAL_REQUEST':
			# add initial game state data
			self.sharedData['currentGameState'].aangPlayerNumber = self.sharedData['currentMenuState'].aangPlayerNumber
			self.sharedData['currentGameState'].kataraPlayerNumber = self.sharedData['currentMenuState'].kataraPlayerNumber
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
	# keep connections
	player1Connection = None
	player2Connection = None

	def __init__(self, dataDict):
		self.sharedData = dataDict

	def buildProtocol(self, addr):
		# determine who is player1 by connection order
		if self.player1Connection is None:
			self.player1Connection = GameConnection(self.sharedData)
			self.player1Connection.playerNumber = 1
			return self.player1Connection
		else:
			self.player2Connection = GameConnection(self.sharedData)
			self.player2Connection.playerNumber = 2
			return self.player2Connection

class ChatConnection(LineReceiver):
	def __init__(self, dataDict):
		self.sharedData = dataDict

	def connectionMade(self):
		# inform lovers of connection or inform that lover hasn't connected
		if self.sharedData['currentChatFactory'].firstPlayerConnection is not None and self.sharedData['currentChatFactory'].secondPlayerConnection is not None:
			self.sharedData['currentChatFactory'].firstPlayerConnection.sendLine("Your lover has connected")
			self.sharedData['currentChatFactory'].secondPlayerConnection.sendLine("Your lover has connected")
		else:
			self.sendLine("Your lover has not yet connected")

	def lineReceived(self, line):
		#first check if the other player has connected
		if self.sharedData['currentChatFactory'].firstPlayerConnection is not None and self.sharedData['currentChatFactory'].secondPlayerConnection is not None:
			#pass it on
			if self.sharedData['currentChatFactory'].firstPlayerConnection == self:
				#send to the other player
				self.sharedData['currentChatFactory'].secondPlayerConnection.sendLine(line)
			else:
				self.sharedData['currentChatFactory'].firstPlayerConnection.sendLine(line)
		else:			
			self.sendLine("Your lover has not yet connected")

class ChatConnectionFactory(Factory):
	# not necessarily players one and two, depending on connection time
	firstPlayerConnection = None
	secondPlayerConnection = None

	def __init__(self, dataDict):
		self.sharedData = dataDict

	def buildProtocol(self, addr):
		# choose first and second player based on connection order
		if self.firstPlayerConnection is None:
			self.firstPlayerConnection = ChatConnection(self.sharedData)
			self.firstPlayerConnection.playerNumber = 1
			return self.firstPlayerConnection
		else:
			self.secondPlayerConnection = ChatConnection(self.sharedData)
			self.secondPlayerConnection.playerNumber = 2
			return self.secondPlayerConnection

	def startedConnecting(self, connector):
		pass


# this data is shared among all connections and factories
sharedData = dict()
#state refers to data pertaining to the game
#screen refers to the point of the game
sharedData.update({'currentGameState' : GameState(), 'currentMenuState' : MenuState(), 'currentGameScreen' : 'MENU_SCREEN', "currentChatFactory" : ChatConnectionFactory(sharedData), "currentGameFactory" : GameConnectionFactory(sharedData)})

# listen for player connections
reactor.listenTCP(2580, sharedData["currentGameFactory"])
reactor.listenTCP(2581, sharedData["currentChatFactory"])
reactor.run()