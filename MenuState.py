class MenuState(object):
	playerNumber = 0
	aangPlayer = 0
	kataraPlayer = 0

	def amReady(self):
		return (self.aangPlayer is not 0) and (self.kataraPlayer is not 0)