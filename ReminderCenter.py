"""
A Class that will manage a collection of Reminder objects
so that we can easily, add, remove, and cancel the different
Reminders.
"""

from Reminder.py import Reminder

class ReminderCenter(object):
	def __init__(self):
		self.reminders = dict();

	def addReminder(self, user_name, user_id, message, seconds):
		reminder = new Reminder(user_name, user_id, message, seconds)
		reminder.subscribe(removeReminder)
		self.reminders[custom_id] = reminder
		reminder.startReminder

	def removeReminder(self, message):
		try:
			del self.reminders[message]
		except:
			# If we hit here, then the reminder doesn't
			# exist here and we don't need to worry about
			# it.
			pass