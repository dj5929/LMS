class Books():
	id = 0
	name = ""
	edition = ""
	year = ""
	count = 1
	availability = False

	course = {}

	def __init__(self, BookDAO):
		self.dao = BookDAO