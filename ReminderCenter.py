"""
A Class that will manage a collection of Reminder objects
so that we can easily, add, remove, and cancel the different
Reminders.
"""

from reminder import Reminder

class ReminderCenter(object):
	def __init__(self):
		self.reminders = [];

	def addReminder(self, user_name, user_id, message, seconds):
		reminder = new Reminder(user_name, user_id, message, seconds)
		reminder.subscribe(removeReminder)
		self.reminders.append(reminder)
		reminder.startReminder

	def removeReminder(self, index):
		try:
			del self.reminders[index]
		except:
			# If we hit here, then the reminder doesn't
			# exist here and we don't need to worry about
			# it.
			pass