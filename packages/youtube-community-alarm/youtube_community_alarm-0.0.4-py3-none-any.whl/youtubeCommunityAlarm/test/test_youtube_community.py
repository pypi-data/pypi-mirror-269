import unittest
from unittest.mock import patch
from youtubeCommunityAlarm.youtube_community import YoutubeCommunity


class TestYoutubeCommunity(unittest.TestCase):
    @patch('youtubeCommunityAlarm.youtube_community.requests.get')
    def test_get_all_posts_with_time(self, mock_get):
        # Mock response
        mock_get.return_value.status_code = 200
        # read test_youtube_community_response.html
        with open("youtubeCommunityAlarm/test/test_youtube_community_response.html", "r", encoding="utf-8") as file:
            mock_get.return_value.text = file.read()

        # Initialize YoutubeCommunity object with a dummy channel_id
        youtube_community = YoutubeCommunity("@bdns")

        # Call the method under test
        posts_with_time = youtube_community.get_all_posts_with_time()

        # Assert the result
        self.assertEqual(len(posts_with_time), 10)
        self.assertEqual(posts_with_time[0], ("5일 전", "직장에서 하면 큰일나는 것은?"))

    @patch('youtubeCommunityAlarm.youtube_community.requests.get')
    def test_get_all_posts_with_time_no_data(self, mock_get):
        # Mock response with status code other than 200
        mock_get.return_value.status_code = 404

        # Initialize YoutubeCommunity object with a dummy channel_id
        youtube_community = YoutubeCommunity("@bdns")

        # Call the method under test
        posts_with_time = youtube_community.get_all_posts_with_time()

        # Assert that empty list is returned
        self.assertEqual(posts_with_time, [])


if __name__ == '__main__':
    unittest.main()
