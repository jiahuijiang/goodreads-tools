import os
import json
import random
import time
from bs4 import BeautifulSoup
from goodreads import Goodreads
from environment import cached_friends_path


def get_all_friends_id(force_reload=False):
    print("Getting all friends...")
    if force_reload is True or os.path.exists(cached_friends_path) is False:
        friends = {}
        page_no = 1
        while True:
            print("Loading page " + str(page_no) + "...", end='\r')
            friend_ids_in_page = get_friends_page(page_no)
            if not friend_ids_in_page:
                break
            friends.update(friend_ids_in_page)
            page_no = page_no + 1
            time.sleep(random.randint(0, 2))
        save_to_cache(friends)
        return friends
    else:
        return load_from_cache()


def load_from_cache():
    if os.path.exists(cached_friends_path):
        with open(cached_friends_path, 'r') as f:
            return json.loads(f.read())
    return []


def save_to_cache(friends):
    with open(cached_friends_path, 'w') as f:
        json.dump(friends, f)


def get_friends_page(page_no):
    url = f"https://www.goodreads.com/friend?page={page_no}&ref=nav_my_friends"
    content = Goodreads().make_request(url)

    soup = BeautifulSoup(content, 'html.parser')

    users = {}
    for user_link_tag in soup.find_all(class_='userLink'):
        try:
            user_link = user_link_tag['href']
            user_id = user_link[user_link.rindex("/") + 1: user_link.find("-")]
            user_name = user_link_tag.contents[0]
            users[user_id] = user_name
        except:
            print(f'cannot parse {user_link}')

    return users
