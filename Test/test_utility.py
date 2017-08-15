"""
Python unit test file that will test the utility.py
file. 
"""

import pytest, mock # Test library and mocking
import utility # What we're testing
import requests, praw, os, random # libraries used, that we need to mock.


class TestBotMessage(object):

	@mock.patch.object(requests, 'post')
	@mock.patch.object(os.environ, 'get')
	def test_botMessage(self,  environ_get, requests_post):

		# Setup the expected return values
		message = 'This is a test message'
		expected_values = {
			'bot_id': '12345',
			'text': message
		}

		# Setup the mock objects
		requests_post.return_value = True
		environ_get.return_value = '12345'		

		# Call the test function!
		utility.botMessage(message)

		# Ensure that the mocked functions were called
		# and with the correct arguments
		environ_get.assert_called_once_with('BOT_ID')
		requests_post.assert_called_once_with(utility.GROUPME_BOT_PATH + 'post',
											  data=expected_values)


class TestInvalidSearch(object):

	@mock.patch.object(utility, 'botMessage')
	@mock.patch.object(random, 'choice')
	def test_invalidSearch(self, random_choice, utility_botMessage):
		
		# Expected values
		message = 'This is a test message'

		# Setup the mock objects
		random_choice.return_value = message
		utility_botMessage.return_value = True
		mock_open = mock.mock_open()

		with mock.patch("builtins.open", mock_open, create=True):
			# Call the test function
			utility.invalidSearch()

			# Ensure that the mocked functions were called and with
			# the correct arguments
			mock_open.assert_called_once_with('failed_search.txt')
			random_choice.assert_called_once()
			utility_botMessage.assert_called_once_with(message)


class TestObtainHotSubmission(object):

	def test_obtainHotSubmissions(self):
		assert(True)
