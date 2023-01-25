import logging
from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup


class Friends:
    url = "https://www.goodreads.com/friend?page=5&ref=nav_my_friends"