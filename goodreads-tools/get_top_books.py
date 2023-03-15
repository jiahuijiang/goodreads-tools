import os
import json
from bs4 import BeautifulSoup
from goodreads import Goodreads
from environment import cached_top_book_dir, cached_top_book_path
from rating_parser import rating_by_comment

goodreads = Goodreads()


def get_friends_top_books(user_ids, force_reload=False):
    print(f"Getting top books for {len(user_ids)} users...")
    if not os.path.exists(cached_top_book_dir):
        os.makedirs(cached_top_book_dir)

    top_books = {}
    for index, user_id in enumerate(user_ids):
        print(f"Getting top books for user {index + 1}/{len(user_ids)}...", end='\r')
        top_books[user_id] = get_friend_top_books(user_id, force_reload)
    print("Getting top books for users completed.")
    return top_books


def get_friend_top_books(user_id, force_reload=False):
    print(f"Getting top books for user {user_id}...")
    if force_reload is True or os.path.exists(cached_top_book_path(user_id)) is False:
        top_books = parse_top_books(user_id)
        save_to_cache(user_id, top_books)
        return top_books
    else:
        return load_from_cache(user_id)


def parse_top_books(user_id):
    url = f"https://www.goodreads.com/review/list/{user_id}?shelf=read&sort=rating&per_page=100"
    content = goodreads.make_request(url)
    soup = BeautifulSoup(content, 'html.parser')
    top_books = []

    book_reviews = soup.find_all("tr", {"class": "bookalike review"})

    for book_review in book_reviews:
        try:
            their_review = book_review\
                .find("td", {"class": "field rating"})\
                .find("span", {"class": "staticStars notranslate"}).get("title", None)
            # is their top book
            if their_review is not None:
                their_rating = rating_by_comment.get(their_review, 0)
                if their_rating >= 4:
                    my_review = book_review\
                        .find("td", {"class": "field shelves"})\
                        .find("div", {"class": "stars"})["data-rating"]
                    # I haven't read the book yet
                    if int(my_review) == 0:
                        book_title_and_link = book_review \
                            .find("td", {"class": "field title"})\
                            .find("a")
                        top_books.append({
                            "url": get_full_url(book_title_and_link["href"]),
                            "title": book_title_and_link["title"],
                            "rating": their_rating
                        })
        except Exception as e:
            print(e)
            print(book_review)
            raise e
    return top_books


def get_full_url(partial_url):
    return "https://www.goodreads.com" + partial_url


def save_to_cache(user_id, top_books):
    if not os.path.exists(cached_top_book_dir):
        os.makedirs(cached_top_book_dir)
    with open(cached_top_book_path(user_id), 'w') as f:
        json.dump(top_books, f)


def load_from_cache(user_id):
    if os.path.exists(cached_top_book_path(user_id)):
        with open(cached_top_book_path(user_id), 'r') as f:
            return json.loads(f.read())
    return []