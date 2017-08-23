"""
Python unit test file that will test the utility.py
file. 
"""

import pytest, mock # Test library and mocking
import utility # What we're testing
import requests, praw, os, random # libraries used, that we need to mock.

def os_get_side_effect(arg):
	values = {
		'BOT_ID': 'bot_id',
		'GIPHY_KEY': 'giphy_key',
		'GROUPME_TOKEN': 'groupme_token',
		'REDDIT_CLIENT_ID': 'reddit_client_id',
		'REDDIT_CLIENT_SECRET': 'reddit_client_secret',
		'REDDIT_PASSWORD': 'reddit_password',
		'REDDIT_USERNAME': 'reddit_username',
		'USER_AGENT': 'user_agent'
	}

	try:
		return values[arg]
	except:
		return ''

class TestBotMessage(object):
	
	@mock.patch.object(requests, 'post')
	@mock.patch.object(os.environ, 'get')
	def test_botMessage(self,  environ_get, requests_post):

		# Setup the expected return values
		message = 'This is a test message'
		expected_values = {
			'bot_id': 'bot_id',
			'text': message
		}

		# Setup the mock objects
		requests_post.return_value = True
		environ_get.side_effect = os_get_side_effect	

		# Call the test function!
		utility.botMessage(message)

		# Ensure that the mocked functions were called
		# and with the correct arguments
		environ_get.assert_called_once_with('BOT_ID')
		requests_post.assert_called_once_with(utility.GROUPME_BOT_PATH + 'post',
											  data=expected_values)

	@mock.patch.object(requests, 'post')
	@mock.patch.object(os.environ, 'get')
	def test_botMessage_empty_string(self,  environ_get, requests_post):

		# Setup the expected return values
		message = ''
		expected_values = {
			'bot_id': 'bot_id',
			'text': message
		}

		# Setup the mock objects
		requests_post.return_value = True
		environ_get.side_effect = os_get_side_effect	

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

	def setup(self):
		"""
		Setup the shared mock objects that's in both the side effect
		and needs to be checked by the assert.

		This is run before every test
		"""		
		self.hot_mock = mock.Mock()
		self.side_effect_subreddit = mock.Mock()
		self.side_effect_subreddit.hot = self.hot_mock

	def subreddit_side_effect(self, arg):
		# Side effect function that is used when the subreddit.hot
		# is called
		if arg:
			# we just want to continue on
			return self.side_effect_subreddit
		else:
			raise TypeError()

	@mock.patch.object(praw, 'Reddit')
	@mock.patch.object(os.environ, 'get')
	def test_obtainHotSubmissions_with_r_slash(self, environ_get, mock_praw):
		
		# Setup expected values and the call values
		subreddit_call = 'r/Test'
		expected_subreddit_call = 'Test'
		limit = 1 # 1 is the default value of the function call

		# Setup mock objects
		environ_get.side_effect = os_get_side_effect

		# Setup the mock objects from the ground up.
		self.hot_mock.return_value = [True] * limit

		subreddit_mock = mock.Mock()
		subreddit_mock.side_effect = self.subreddit_side_effect

		reddit_mock = mock.Mock()
		reddit_mock.subreddit = subreddit_mock

		# Actually set up the return of the praw to be the mock objects
		mock_praw.return_value = reddit_mock

		# call the function
		returned_value = utility.obtainHotSubmissions(subreddit_call, 
													  num_of_sub=limit)

		# make sure that the functions were called the correct number
		# of times and with the correct arguments
		assert(environ_get.call_count == 5)	# os.envrion.get
		mock_praw.assert_called_once_with(  # praw.Reddit
			client_id='reddit_client_id',
			client_secret='reddit_client_secret',			
			user_agent='user_agent',
			username='reddit_username',
			password='reddit_password'
		)
		reddit_mock.subreddit.assert_called_once_with(expected_subreddit_call)
		self.side_effect_subreddit.hot.assert_called_once_with(limit=limit)
		assert(len(returned_value) == limit)

	@mock.patch.object(praw, 'Reddit')
	@mock.patch.object(os.environ, 'get')
	def test_obtainHotSubmissions_without_r_slash(self, 
												  environ_get, 
												  mock_praw):
		
		# Setup expected values and the call values
		subreddit_call = 'Test'
		expected_subreddit_call = 'Test'
		limit = 1 # 1 is the default value of the function call

		# Setup mock objects
		environ_get.side_effect = os_get_side_effect

		# Setup the mock objects from the ground up.
		self.hot_mock.return_value = [True] * limit

		subreddit_mock = mock.Mock()
		subreddit_mock.side_effect = self.subreddit_side_effect

		reddit_mock = mock.Mock()
		reddit_mock.subreddit = subreddit_mock

		# Actually set up the return of the praw to be the mock objects
		mock_praw.return_value = reddit_mock

		# call the function
		returned_value = utility.obtainHotSubmissions(subreddit_call, 
													  num_of_sub=limit)

		# make sure that the functions were called the correct number
		# of times and with the correct arguments
		assert(environ_get.call_count == 5)	# os.envrion.get
		mock_praw.assert_called_once_with(  # praw.Reddit
			client_id='reddit_client_id',
			client_secret='reddit_client_secret',			
			user_agent='user_agent',
			username='reddit_username',
			password='reddit_password'
		)
		reddit_mock.subreddit.assert_called_once_with(expected_subreddit_call)
		self.side_effect_subreddit.hot.assert_called_once_with(limit=limit)
		assert(len(returned_value) == limit)

	@mock.patch.object(praw, 'Reddit')
	@mock.patch.object(os.environ, 'get')
	def test_obtainHotSubmissions_with_0_limit(self, environ_get, mock_praw):
		
		# Setup expected values and the call values
		subreddit_call = 'r/Test'
		expected_subreddit_call = 'Test'
		limit = 0 # 1 is the default value of the function call

		# Setup mock objects
		environ_get.side_effect = os_get_side_effect

		# Setup the mock objects from the ground up.
		self.hot_mock.return_value = [True] * limit

		subreddit_mock = mock.Mock()
		subreddit_mock.side_effect = self.subreddit_side_effect

		reddit_mock = mock.Mock()
		reddit_mock.subreddit = subreddit_mock

		# Actually set up the return of the praw to be the mock objects
		mock_praw.return_value = reddit_mock

		# call the function
		returned_value = utility.obtainHotSubmissions(subreddit_call, 
													  num_of_sub=limit)

		# make sure that the functions were called the correct number
		# of times and with the correct arguments
		assert(environ_get.call_count == 5)	# os.envrion.get
		mock_praw.assert_called_once_with(  # praw.Reddit
			client_id='reddit_client_id',
			client_secret='reddit_client_secret',			
			user_agent='user_agent',
			username='reddit_username',
			password='reddit_password'
		)
		reddit_mock.subreddit.assert_called_once_with(expected_subreddit_call)
		self.side_effect_subreddit.hot.assert_called_once_with(limit=limit)
		assert(len(returned_value) == limit)	

	@mock.patch.object(praw, 'Reddit')
	@mock.patch.object(os.environ, 'get')
	def test_obtainHotSubmissions_with_higher_limit(self, 
													environ_get,
													mock_praw):
		
		# Setup expected values and the call values
		subreddit_call = 'r/Test'
		expected_subreddit_call = 'Test'
		limit = 5 # 1 is the default value of the function call

		# Setup mock objects
		environ_get.side_effect = os_get_side_effect

		# Setup the mock objects from the ground up.
		self.hot_mock.return_value = [True] * limit

		subreddit_mock = mock.Mock()
		subreddit_mock.side_effect = self.subreddit_side_effect

		reddit_mock = mock.Mock()
		reddit_mock.subreddit = subreddit_mock

		# Actually set up the return of the praw to be the mock objects
		mock_praw.return_value = reddit_mock

		# call the function
		returned_value = utility.obtainHotSubmissions(subreddit_call, 
													  num_of_sub=limit)

		# make sure that the functions were called the correct number
		# of times and with the correct arguments
		assert(environ_get.call_count == 5)	# os.envrion.get
		mock_praw.assert_called_once_with(  # praw.Reddit
			client_id='reddit_client_id',
			client_secret='reddit_client_secret',			
			user_agent='user_agent',
			username='reddit_username',
			password='reddit_password'
		)
		reddit_mock.subreddit.assert_called_once_with(expected_subreddit_call)
		self.side_effect_subreddit.hot.assert_called_once_with(limit=limit)
		assert(len(returned_value) == limit)

	@mock.patch.object(praw, 'Reddit')
	@mock.patch.object(os.environ, 'get')
	def test_obtainHotSubmissions_empty_string(self, environ_get, mock_praw):
		
		# Setup expected values and the call values
		subreddit_call = ''
		expected_subreddit_call = ''
		limit = 5 # 1 is the default value of the function call

		# Setup mock objects
		environ_get.side_effect = os_get_side_effect

		# Setup the mock objects from the ground up.
		self.hot_mock.return_value = [True] * limit

		subreddit_mock = mock.Mock()
		subreddit_mock.side_effect = self.subreddit_side_effect

		reddit_mock = mock.Mock()
		reddit_mock.subreddit = subreddit_mock

		# Actually set up the return of the praw to be the mock objects
		mock_praw.return_value = reddit_mock

		# call the function
		with pytest.raises(TypeError) as e_info:
			returned_value = utility.obtainHotSubmissions(subreddit_call, 
														  num_of_sub=limit)

		# make sure that the functions were called the correct number
		# of times and with the correct arguments
		assert(environ_get.call_count == 5)	# os.envrion.get
		mock_praw.assert_called_once_with(  # praw.Reddit
			client_id='reddit_client_id',
			client_secret='reddit_client_secret',			
			user_agent='user_agent',
			username='reddit_username',
			password='reddit_password'
		)
		reddit_mock.subreddit.assert_called_once_with(expected_subreddit_call)
		self.side_effect_subreddit.hot.assert_not_called()