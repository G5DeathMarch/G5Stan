"""
Class that will be used to remind the user, after a specified
amount of time to give some specified message.
"""
from utility import mention
from threading import Timer

class Reminder(Observable):
	
	def __init__(self, user_name, uid, reminder, timeout):
		super().__init__(self)
		self.timeout = timeout
		self.uid = uid
		self.user_name = user_name
		self.message = '@{0} {1}'.format(user_name, reminder)

	def remind(self):
		mention(self.message, [0, len(user_name) + 1], [self.uid])
		super().notify(self, message=self.message)

	def start_reminder(self):
		Timer(self.timeout, remind).start()