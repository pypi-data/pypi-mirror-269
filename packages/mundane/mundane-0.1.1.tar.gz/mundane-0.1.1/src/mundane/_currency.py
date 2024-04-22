class Currency(type):

	@classmethod
	def __prepare__(cls, name: str, bases: tuple[type, ...], /, **kwds: object):
		namespace = super().__prepare__(name, bases, **kwds)
		namespace['__slots__'] = ()
		return namespace

	def __str__(self):
		return self.__name__

	def __repr__(self):
		return f"'{self.__name__}'"

	def __hash__(self):
		return hash(self.__name__)

	def __eq__(self, other: object):
		return self.__name__ == other if isinstance(other, str) else super().__eq__(other)
