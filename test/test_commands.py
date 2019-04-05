"""
Python unit test file that will test
commands.py file
"""

import pytest  # test library
from .helpers import *
from mock import Mock, mock, call  # mocking library
import commands  # What we're testing
# Libraries / code we're going to be mocking
import os
import requests
import random

test_resources_root = os.path.join(os.path.dirname(__file__), 'resources')


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
        commands.get_image(self.search_term, self.num_of_gifs)

        # Verify Mocks
        """
        We use the has_calls with any_order=True because the system could
        call the mock multiple times. So we can't just have a called_once_with
        because it will fail.
        """
        environ_get.assert_has_calls([call('GIPHY_KEY')], any_order=True)
        requests_get.assert_called_once_with(self.url, params=self.expected_payload)
        random_choice.assert_called_once_with(json_data)
        mock_bot_message.assert_called_once_with(returned_url)

    @mock.patch('commands.invalid_search')
    @mock.patch.object(requests, 'get')
    @mock.patch.object(os.environ, 'get')
    def test_get_image_requests_throw_exception(self, environ_get, requests_get, mock_invalid_search):
        environ_get.side_effect = os_get_side_effect
        requests_get.side_effect = Mock(side_effect=requests.RequestException)

        # Call test function
        commands.get_image(self.search_term, self.num_of_gifs)

        # Verify Mocks
        environ_get.assert_has_calls([call('GIPHY_KEY')], any_order=True)
        requests_get.assert_called_once_with(self.url, params=self.expected_payload)
        mock_invalid_search.assert_called_once()

    @mock.patch.object(os.environ, 'get')
    def test_get_image_no_environment_key(self, environ_get):
        # Setup Mock
        environ_get.side_effect = Mock(side_effect=KeyError)

        # Call test function
        with pytest.raises(KeyError):
            commands.get_image(self.search_term, self.num_of_gifs)


class TestCheerUp(object):
    def setup(self):
        self.compliments_file = os.path.join(test_resources_root, 'test_compliments.txt')

    @mock.patch('commands.bot_message')
    def test_cheer_up_get_compliments_from_file(self, bot_message_mock):
        expected_cheer_up = "test"

        # Call test function
        commands.cheer_up(self.compliments_file)

        # Verify Mocks
        bot_message_mock.assert_called_once_with(expected_cheer_up)

    @mock.patch('commands.bot_message')
    def test_cheer_up_should_error_on_file_that_doesnt_exist(self, bot_message_mock):
        filename = 'totally_not_a_file'

        # Call test function
        with pytest.raises(FileNotFoundError):
            commands.cheer_up(filename)

        # Verify Mocks
        bot_message_mock.assert_not_called()


class TestHelpMeStan(object):
    def setup(self):
        self.readme = os.path.join(test_resources_root, 'test_readme.txt')

    @mock.patch('commands.bot_message')
    def test_help_me_stan_reads_commands(self, mock_bot_message):
        expected_return = '\n'.join(['test1', 'test2', 'test3'])

        # Call Test Function
        commands.help_me_stan(self.readme)

        # Verify Mocks
        mock_bot_message.assert_called_once_with(expected_return.strip())

    @mock.patch('commands.bot_message')
    def test_help_me_stan_throws_error_when_file_doesnt_exist(self, mock_bot_message):
        file = 'totally_not_a_file'

        # Call Test Function
        with pytest.raises(FileNotFoundError):
            commands.help_me_stan(file)

        # Verify Mocks
        mock_bot_message.assert_not_called()

    @mock.patch('commands.bot_message')
    def test_help_me_stan_no_commands_in_file(self, mock_bot_message):
        empty_file = os.path.join(test_resources_root, 'empty_file.txt')

        # Call Test Function
        commands.help_me_stan(empty_file)

        # Verify Mocks
        mock_bot_message.assert_called_once_with('')


class TestEyeBleach(object):

    class fake_reddit_post(object):
        def __init__(self, url):
            self.url = url

    @mock.patch('commands.bot_message')
    @mock.patch('commands.obtain_hot_submissions')
    def test_eye_bleach_only_gets_non_reddit_com_urls(self, mock_hot_submissions, mock_bot_message):
        returned = [
            self.fake_reddit_post('something.reddit.com'),
            self.fake_reddit_post('valid.com'),
            self.fake_reddit_post('another.reddit.com'),
            self.fake_reddit_post('another.reddit.com'),
            self.fake_reddit_post('valid.com')
        ]

        expected_calls = [
            call('valid.com'),
            call('valid.com')
        ]

        # Setup Mocks
        mock_hot_submissions.return_value = returned

        # Call Test function
        commands.eye_bleach()

        # Verify Mocks
        assert(mock_bot_message.call_args_list == expected_calls)

    @mock.patch('commands.bot_message')
    @mock.patch('commands.obtain_hot_submissions')
    def test_eye_bleach_only_gets_a_max_of_3_urls(self, mock_hot_submissions, mock_bot_message):
        returned = [
            self.fake_reddit_post('valid.com'),
            self.fake_reddit_post('valid.com'),
            self.fake_reddit_post('valid.com'),
            self.fake_reddit_post('valid.com'),
            self.fake_reddit_post('valid.com')
        ]

        expected_calls = [
            call('valid.com'),
            call('valid.com'),
            call('valid.com')
        ]

        # Setup Mock
        mock_hot_submissions.return_value = returned

        # Call Test Method
        commands.eye_bleach()

        # Verify Mock
        assert(mock_bot_message.call_args_list == expected_calls)

    @mock.patch('commands.bot_message')
    @mock.patch('commands.obtain_hot_submissions')
    def test_eye_bleach_reddit_returns_nothing(self, mock_hot_submissions, mock_bot_message):
        returned = [
            self.fake_reddit_post('reddit.com'),
            self.fake_reddit_post('reddit.com'),
            self.fake_reddit_post('reddit.com'),
            self.fake_reddit_post('reddit.com'),
            self.fake_reddit_post('reddit.com')
        ]

        # Setup Mock
        mock_hot_submissions.return_value = returned

        # Call Test Method
        commands.eye_bleach()

        # Verify Mock
        mock_bot_message.assert_not_called()


class TestCrellPic(object):
    def setup(self):
        self.image_file = os.path.join(test_resources_root, 'test_crell_images.txt')

    @mock.patch('commands.bot_image_message')
    def test_crell_pic_chooses_image_from_file(self, mock_bot_image_message):
        commands.crell_pic(self.image_file)

        # Verify Mock
        mock_bot_image_message.assert_called_once_with('test_image_to_use')

    @mock.patch('commands.bot_image_message')
    def test_crell_pic_throws_error_when_theres_no_file(self, mock_bot_image_message):
        with pytest.raises(FileNotFoundError):
            commands.crell_pic('NOT_A_FILE')

        # Verify Mock
        mock_bot_image_message.assert_not_called()