class Person:
	def __init__(self,name,address):
		print("this is person")
		self.name=name
		self.address = address 
class SSC:
	def __init__(self, grade):
		print("this is SSC")
		self.grade=grade
class Inter(SSC, Person):
	def __init__(self, grade, name, address):
		self.grade=grade
		super().__init__(name, address)
	def get(self):
		return self.__dict__
sai=Inter(23,"SAI","ad1")
print(sai.get())
