import requests
import os


class Goodreads:

    user_id = os.getenv('GOODREADS_USER_ID')  # None
    user_password = os.environ.get('GOODREADS_USER_PASSWORD')  # None

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36 QIHU 360SE',
        'Cookie': f'u={user_id}; p={user_password};'
    }

    def make_request(self, url):
        response = requests.get(url, headers=self.headers)
        return response.content

