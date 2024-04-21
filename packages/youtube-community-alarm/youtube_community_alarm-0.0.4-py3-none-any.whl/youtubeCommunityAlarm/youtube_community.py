import requests
import json
import re
from retry import retry
from requests.exceptions import SSLError
from urllib3.exceptions import MaxRetryError

BASE_URL = "https://www.youtube.com/"
COMMUNITY = "커뮤니티"
COMMUNITY_TAB_NUMBER = -2   # 뒤에서 두번째 tab
REGEX = {
    "YT_INITIAL_DATA": "ytInitialData = ({(?:(?:.|\n)*)?});</script>",
    "HOUR_TIME_PATTERN": r'(\d+)\s*시간\s*전',
    "MINUTE_TIME_PATTERN": r'(\d+)\s*분\s*전',
}


class YoutubeCommunity:
    def __init__(self, channel_id):
        self.channel_id = channel_id

    def find_community_tab(self, tabs) -> dict:
        for tab in tabs:
            if tab['tabRenderer']['title'] == COMMUNITY:
                return tab

        return {}

    @retry((SSLError, MaxRetryError), tries=3, delay=2)
    def get_all_posts_with_time(self):
        response = requests.get(f"{BASE_URL + self.channel_id}/community")
        posts_with_time = []
        if response.status_code == 200:
            m = re.findall(REGEX["YT_INITIAL_DATA"], response.text)
            if m:
                json_data = json.loads(m[0])
            else:
                print("Regular expression did not match any content in the response text.")
                return []

            tabs = json_data['contents']['twoColumnBrowseResultsRenderer']['tabs']
            tab = tabs[COMMUNITY_TAB_NUMBER]

            if tab['tabRenderer']['title'] != COMMUNITY:
                tab = self.find_community_tab(tabs)

            posts = tab['tabRenderer']['content']['sectionListRenderer']['contents'][0]['itemSectionRenderer']['contents']
            if not posts:
                print("No posts found.")
                return

            for post in posts:
                try:
                    back_stage_post_renderer = post["backstagePostThreadRenderer"]["post"]['backstagePostRenderer']
                    text = back_stage_post_renderer["contentText"]["runs"][0]["text"]
                    time = back_stage_post_renderer["publishedTimeText"]["runs"][0]["text"]
                    posts_with_time.append((time, text))
                except KeyError:
                    continue
        else:
            print(f"[Can't get data from the channel_id: {self.channel_id}]")
            print(f"Response status code: {response.status_code}")

        return posts_with_time
