class Player:
	
	def setName(self, name):
		self.name = name.capitalize()
		
	def getName(self):
		return self.name
		
	def setDesc(self, desc):
		self.desc = desc.capitalize()
		
	def getDesc(self):
		return self.desc
		
player1 = Player()
player1.setName('inkon')
player1.setDesc('short, stocky and mean')
character_sheet = """
Name: {0!s}
Desc: {1!s}
""".format(player1.getName(), player1.getDesc())
print(character_sheet)
