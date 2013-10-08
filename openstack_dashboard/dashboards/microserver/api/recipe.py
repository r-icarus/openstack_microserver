from datetime import datetime

class Recipe(object):
	def __init__(self, recipe_id=0, name = "", recipe_type = ""):
		self._id = recipe_id
		self._name = name
		self._recipe_type = recipe_type
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
	def created_at(self):
		return self._created_at

def recipe_list():
	recipe_list = [ Recipe(1,"SotolBlog","wordpress"), Recipe(2,"SotolMail", "Postfix")]
	return recipe_list
