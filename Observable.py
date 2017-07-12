"""
Event class that we'll set the attributes on it
so that we can pass whatever information we 
want back to the observer
"""
class Event(object):
	pass

"""
Observable Class that will hold a list of callbacks
that we'll send our event with all of our attributes to
"""
class Observable(object):
	def __init__(self):
		self.callbacks = []
	def subscribe(self, callback):
		self.callbacks.append(callback)
	def notify(self, **attrs):
		e = Event()
		e.source = self
		for key, value in attrs.items():
			setattr(e, key, value)
		for func in self.callbacks:
			func(e)
