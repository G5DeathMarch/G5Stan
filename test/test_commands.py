"""
Python unit test file that will test
commands.py file
"""

import pytest  # test library
from test.helpers import *
from mock import Mock, mock, call  # mocking library
import commands  # What we're testing
# Libraries / code we're going to be mocking
import os
import requests
import random
import utility


class TestGetImage(object):
    def setup(self):
        self.url = "http://api.giphy.com/v1/gifs/search"
        self.search_term = "test"
        self.num_of_gifs = 1
        self.api_key = "giphy_key"

        self.expected_payload = {
            'q': self.search_term,
            'limit': self.num_of_gifs,
            'api_key': self.api_key
        }

    """
    the reason why we patch commands.bot_message instead of utility.bot_message is because our
    import in "commands.py" is "from utility import bot_message" so we need to patch where
    it is looked up, not where it is from.
    
    See here for more info: http://www.voidspace.org.uk/python/mock/patch.html#where-to-patch 
    """
    @mock.patch('commands.bot_message')
    @mock.patch.object(random, 'choice')
    @mock.patch.object(requests, 'get')
    @mock.patch.object(os.environ, 'get')
    def test_get_image(self, environ_get, requests_get, random_choice, mock_bot_message):
        # Setup Mocks
        returned_url = "testurl.com"
        returned_gif = {
            'images': {
                'downsized': {
                    'url': returned_url
                }
            }
        }
        json_data = []

        environ_get.side_effect = os_get_side_effect
        mock_request = Mock()
        mock_request.json.return_value = {'data': json_data}
        requests_get.return_value = mock_request
        random_choice.return_value = returned_gif

        # Call test function
        with mock.patch('utility.bot_message'):
            commands.get_image(self.search_term, self.num_of_gifs)

        # Verify Mocks
        environ_get.assert_has_calls([call('GIPHY_KEY')], any_order=True)
        requests_get.assert_called_once_with(self.url, params=self.expected_payload)
        random_choice.assert_called_once_with(json_data)
        mock_bot_message.assert_called_once_with(returned_url)

    @mock.patch.object(requests, 'get')
    @mock.patch.object(os.environ, 'get')
    def test_get_image_requests_throw_exception(self, environ_get, requests_get,):

        pass

    @mock.patch.object(os.environ, 'get')
    def test_get_image_no_environment_key(self, environ_get):
        # Setup Mock
        environ_get.side_effect = Mock(side_effect=requests.RequestException('Test'))

        # Call test function

        pass


class TestCheerUp(object):
    pass


class TestHelpMeStand(object):
    pass


class TestEyeBleach(object):
    pass


class TestCrellPic(object):
    pass
