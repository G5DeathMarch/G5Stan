"""
Python unit test file that will test the utility.py
file. 
"""

import pytest  # test library
import mock  # mocking library
from test.helpers import *
import utility  # What we're testing
# libraries used, that we need to mock.
import requests
import praw
import os
import random


class TestBotMessage(object):

    def setup(self):
        self.environ_call = 'BOT_ID'

    @mock.patch.object(requests, 'post')
    @mock.patch.object(os.environ, 'get')
    def test_bot_message(self, environ_get, requests_post):
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
        utility.bot_message(message)

        # Ensure that the mocked functions were called
        # and with the correct arguments
        environ_get.assert_called_once_with(self.environ_call)
        requests_post.assert_called_once_with(utility.BASE_URL,
                                              json=expected_values)

    @mock.patch.object(requests, 'post')
    @mock.patch.object(os.environ, 'get')
    def test_bot_message_empty_string(self, environ_get, requests_post):
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
        utility.bot_message(message)

        # Ensure that the mocked functions were called
        # and with the correct arguments
        environ_get.assert_called_once_with(self.environ_call)
        requests_post.assert_called_once_with(utility.BASE_URL,
                                              json=expected_values)


class TestBotImageMessage(object):
    def setup(self):
        self.environ_call = 'BOT_ID'

    @mock.patch.object(requests, 'post')
    @mock.patch.object(os.environ, 'get')
    def test_bot_image_message(self, environ_get, requests_post):
        # Setup Expected Values
        url = 'http://www.greatestUrl.test'
        expected_json = {
            'bot_id': 'bot_id',
            'attachments': [{
                'type': 'image',
                'url': url
            }]
        }

        # Setup mocks
        requests_post.return_value = True
        environ_get.side_effect = os_get_side_effect

        # Call test function
        utility.bot_image_message(url)

        # Verify that our mocks were called as expected and
        # that we send the data needed.
        environ_get.assert_called_once_with(self.environ_call)
        requests_post.assert_called_once_with(utility.BASE_URL,
                                              json=expected_json)

    @mock.patch.object(requests, 'post')
    @mock.patch.object(os.environ, 'get')
    def test_bot_image_message_empty_url(self, environ_get, requests_post):
        # Setup Expected Values
        url = ''
        expected_json = {
            'bot_id': 'bot_id',
            'attachments': [{
                'type': 'image',
                'url': url
            }]
        }

        # Setup mocks
        requests_post.return_value = True
        environ_get.side_effect = os_get_side_effect

        # Call test function
        utility.bot_image_message(url)

        # Verify that our mocks were called as expected and
        # that we send the data needed.
        environ_get.assert_called_once_with(self.environ_call)
        requests_post.assert_called_once_with(utility.BASE_URL,
                                              json=expected_json)

    @mock.patch.object(requests, 'post')
    @mock.patch.object(os.environ, 'get')
    def test_bot_image_message_url_with_extra_spaces(self, environ_get, requests_post):
        # Setup Expected Values
        url = '\t\thttp://www.greatestUrl.test               \n'
        expected_json = {
            'bot_id': 'bot_id',
            'attachments': [{
                'type': 'image',
                'url': 'http://www.greatestUrl.test'  # Notice the lack of whitespace???
            }]
        }

        # Setup mocks
        requests_post.return_value = True
        environ_get.side_effect = os_get_side_effect

        # Call test function
        utility.bot_image_message(url)

        # Verify that our mocks were called as expected and
        # that we send the data needed.
        environ_get.assert_called_once_with(self.environ_call)
        requests_post.assert_called_once_with(utility.BASE_URL,
                                              json=expected_json)


class TestInvalidSearch(object):

    @mock.patch.object(utility, 'bot_message')
    @mock.patch.object(random, 'choice')
    def test_invalid_search(self, random_choice, utility_bot_message):
        # Expected values
        message = 'This is a test message'

        # Setup the mock objects
        random_choice.return_value = message
        utility_bot_message.return_value = True
        mock_open = mock.mock_open()

        with mock.patch("builtins.open", mock_open, create=True):
            # Call the test function
            utility.invalid_search()

            # Ensure that the mocked functions were called and with
            # the correct arguments
            mock_open.assert_called_once_with('failed_search.txt')
            random_choice.assert_called_once()
            utility_bot_message.assert_called_once_with(message)


class TestObtainHotSubmission(object):

    def setup(self):
        """
        Setup the shared mock objects that's in both the side effect
        and needs to be checked by the assert. Also create objects
        that every test will share

        This is run before every test
        """
        self.limit = 1  # by default it is 1

        # The mock objects are built from the ground up

        # Hot function mock
        self.hot_mock = mock.Mock()
        self.hot_mock.return_value = [True] * self.limit

        # subreddit mock
        self.side_effect_subreddit = mock.Mock()
        self.side_effect_subreddit.hot = self.hot_mock

        self.subreddit_mock = mock.Mock()
        self.subreddit_mock.side_effect = self.subreddit_side_effect

        # reddit_mock
        self.reddit_mock = mock.Mock()
        self.reddit_mock.subreddit = self.subreddit_mock

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
    def test_obtain_hot_submissions_with_r_slash(self, environ_get, mock_praw):

        # Setup expected values and the call values
        subreddit_call = 'r/test'
        expected_subreddit_call = 'test'

        # Setup mock objects
        environ_get.side_effect = os_get_side_effect

        # Actually set up the return of the praw to be the mock objects
        mock_praw.return_value = self.reddit_mock

        # call the function
        returned_value = utility.obtain_hot_submissions(subreddit_call,
                                                        num_of_sub=self.limit)

        # make sure that the functions were called the correct number
        # of times and with the correct arguments
        mock_praw.assert_called_once_with(  # praw.Reddit
            client_id='reddit_client_id',
            client_secret='reddit_client_secret',
            user_agent='user_agent',
            username='reddit_username',
            password='reddit_password'
        )
        self.reddit_mock.subreddit.assert_called_once_with(expected_subreddit_call)
        self.hot_mock.assert_called_once_with(limit=self.limit)
        assert (len(returned_value) == self.limit)

    @mock.patch.object(praw, 'Reddit')
    @mock.patch.object(os.environ, 'get')
    def test_obtain_hot_submissions_without_r_slash(self,
                                                    environ_get,
                                                    mock_praw):

        # Setup expected values and the call values
        subreddit_call = 'test'
        expected_subreddit_call = 'test'

        # Setup mock objects
        environ_get.side_effect = os_get_side_effect

        # Actually set up the return of the praw to be the mock objects
        mock_praw.return_value = self.reddit_mock

        # call the function
        returned_value = utility.obtain_hot_submissions(subreddit_call,
                                                      num_of_sub=self.limit)

        # make sure that the functions were called the correct number
        # of times and with the correct arguments
        mock_praw.assert_called_once_with(  # praw.Reddit
            client_id='reddit_client_id',
            client_secret='reddit_client_secret',
            user_agent='user_agent',
            username='reddit_username',
            password='reddit_password'
        )
        self.reddit_mock.subreddit.assert_called_once_with(expected_subreddit_call)
        self.hot_mock.assert_called_once_with(limit=self.limit)
        assert (len(returned_value) == self.limit)

    @mock.patch.object(praw, 'Reddit')
    @mock.patch.object(os.environ, 'get')
    def test_obtain_hot_submissions_with_0_limit(self, environ_get, mock_praw):

        # Setup expected values and the call values
        subreddit_call = 'r/test'
        expected_subreddit_call = 'test'
        self.limit = 0  # 1 is the default value of the function call

        # Setup mock objects
        environ_get.side_effect = os_get_side_effect

        # Change the hot mock's return value
        self.hot_mock.return_value = [True] * self.limit

        # Actually set up the return of the praw to be the mock objects
        mock_praw.return_value = self.reddit_mock

        # call the function
        returned_value = utility.obtain_hot_submissions(subreddit_call,
                                                        num_of_sub=self.limit)

        # make sure that the functions were called the correct number
        # of times and with the correct arguments
        mock_praw.assert_called_once_with(  # praw.Reddit
            client_id='reddit_client_id',
            client_secret='reddit_client_secret',
            user_agent='user_agent',
            username='reddit_username',
            password='reddit_password'
        )
        self.reddit_mock.subreddit.assert_called_once_with(expected_subreddit_call)
        self.hot_mock.assert_called_once_with(limit=self.limit)
        assert (len(returned_value) == self.limit)

    @mock.patch.object(praw, 'Reddit')
    @mock.patch.object(os.environ, 'get')
    def test_obtain_hot_submissions_with_higher_limit(self,
                                                      environ_get,
                                                      mock_praw):

        # Setup expected values and the call values
        subreddit_call = 'r/test'
        expected_subreddit_call = 'test'
        self.limit = 5  # 1 is the default value of the function call

        # Setup mock objects
        environ_get.side_effect = os_get_side_effect

        # Change the hot mock's return value
        self.hot_mock.return_value = [True] * self.limit

        # Actually set up the return of the praw to be the mock objects
        mock_praw.return_value = self.reddit_mock

        # call the function
        returned_value = utility.obtain_hot_submissions(subreddit_call,
                                                        num_of_sub=self.limit)

        # make sure that the functions were called the correct number
        # of times and with the correct arguments
        mock_praw.assert_called_once_with(  # praw.Reddit
            client_id='reddit_client_id',
            client_secret='reddit_client_secret',
            user_agent='user_agent',
            username='reddit_username',
            password='reddit_password'
        )
        self.reddit_mock.subreddit.assert_called_once_with(expected_subreddit_call)
        self.hot_mock.assert_called_once_with(limit=self.limit)
        assert (len(returned_value) == self.limit)

    @mock.patch.object(praw, 'Reddit')
    @mock.patch.object(os.environ, 'get')
    def test_obtain_hot_submissions_empty_string(self, environ_get, mock_praw):

        # Setup expected values and the call values
        subreddit_call = ''
        expected_subreddit_call = ''

        # Setup mock objects
        environ_get.side_effect = os_get_side_effect

        # Actually set up the return of the praw to be the mock objects
        mock_praw.return_value = self.reddit_mock

        # call the function
        with pytest.raises(TypeError) as e_info:
            returned_value = utility.obtain_hot_submissions(subreddit_call,
                                                            num_of_sub=self.limit)

        # make sure that the functions were called the correct number
        # of times and with the correct arguments
        mock_praw.assert_called_once_with(  # praw.Reddit
            client_id='reddit_client_id',
            client_secret='reddit_client_secret',
            user_agent='user_agent',
            username='reddit_username',
            password='reddit_password'
        )
        self.reddit_mock.subreddit.assert_called_once_with(expected_subreddit_call)
        self.hot_mock.assert_not_called()
