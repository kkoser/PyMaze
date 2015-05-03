class MenuState(object):
	aangPlayerNumber = 0
	kataraPlayerNumber = 0
	aangPlayerReady = False
	kataraPlayerReady = False

	def amReady(self):
		return (self.aangPlayer is not 0) and (self.kataraPlayer is not 0)