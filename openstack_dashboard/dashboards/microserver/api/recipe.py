from datetime import datetime

class Recipe(object):
	def __init__(self, recipe_id = 0, name = "", recipe_type = "",status = "" ):
		self._id = recipe_id
		self._name = name
		self._recipe_type = recipe_type
		self._status = status 
		self._created_at = datetime.now()

	@property
	def id(self):
		return self._id

	@property
	def name(self):
		return self._name

	@property
	def recipe_type(self):
		return self._recipe_type

	@property
	def status(self):
		return self._status

	@property
	def created_at(self):
		return self._created_at

SERVER_LIST = [Recipe(1,"SotolBlog","wordpress","Running"), Recipe(2,"SotolMail", "Postfix","Help me :(")]

def recipe_list():
	recipe_list = SERVER_LIST
	return recipe_list

def recipe_status(recipe_id):
	recipe = Recipe(0, 'Not Found', 'Not Found', 'Not Found')
	for server in SERVER_LIST:
		if(server.id == int(recipe_id)):
			recipe = server
	return {'status' : "Nuevo status"}