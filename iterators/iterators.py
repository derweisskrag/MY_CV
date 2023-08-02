class Iterator:
	def __init__(self, data):
		self.data = data
		self.keys_iterator = iter(data.keys())
		self.current_key = None

	def __iter__(self):
		return self

	def __next__(self):
		if self.current_key is None:
			self.current_key = next(self.keys_iterator, None)
		else:
			self.current_key = next(self.keys_iterator, None)

		if self.current_key is None:
			raise StopIteration

		section = self.data[self.current_key]
		return section