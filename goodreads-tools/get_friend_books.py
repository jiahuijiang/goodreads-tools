import os
import json
from bs4 import BeautifulSoup
from goodreads import Goodreads, get_my_id
from environment import cached_top_book_dir, cached_top_book_path
from rating_parser import rating_by_comment

goodreads = Goodreads()


def get_friends_top_books(user_ids, force_reload=False, verbose=False):
    if force_reload is True or verbose is True:
        print(f"Getting top books for {len(user_ids)} users...")
    if not os.path.exists(cached_top_book_dir):
        os.makedirs(cached_top_book_dir)

    top_books = {}
    for index, user_id in enumerate(user_ids):
        if force_reload is True or verbose is True:
            print(f"Getting top books for user {index + 1}/{len(user_ids)}...", end='\r')
        top_books[user_id] = get_friend_top_books(user_id, force_reload)

    if force_reload is True or verbose is True:
        print("Getting top books for users completed.")
    return top_books


def get_friend_top_books(user_id, force_reload=False, verbose=False):
    if force_reload is True or verbose is True:
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
            their_review_stars = book_review\
                .find("td", {"class": "field rating"})\
                .find("span", {"class": "staticStars notranslate"})
            if their_review_stars is not None:
                their_review = their_review_stars.get("title", None)
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
                                "partial_url": book_title_and_link["href"],
                                "title": book_title_and_link["title"],
                                "rating": their_rating
                            })
        except Exception as e:
            print(e)
            print(book_review)
            raise e
    return top_books


def get_my_top_books(force_reload=False, verbose=False):
    my_id = get_my_id()
    if force_reload is True or verbose is True:
        print(f"Getting top books for me...")
    if force_reload is True or os.path.exists(cached_top_book_path(my_id)) is False:
        top_books = parse_my_top_books()
        save_to_cache(my_id, top_books)
        return top_books
    else:
        return load_from_cache(my_id)


def parse_my_top_books():
    my_id = get_my_id()

    url = f"https://www.goodreads.com/review/list/{my_id}?shelf=read&sort=rating&per_page=100"
    content = goodreads.make_request(url)
    soup = BeautifulSoup(content, 'html.parser')
    top_books = []

    book_reviews = soup.find_all("tr", {"class": "bookalike review"})

    for book_review in book_reviews:
        try:
            my_rating = book_review.find("div", {"class": "stars"})["data-rating"]

            # is my top book
            if my_rating is not None:
                if int(my_rating) >= 4:
                    book_title_and_link = book_review \
                        .find("td", {"class": "field title"})\
                        .find("a")
                    top_books.append({
                        "partial_url": book_title_and_link["href"],
                        "title": book_title_and_link["title"],
                        "rating": int(my_rating)
                    })
        except Exception as e:
            print(e)
            print(book_review)
            raise e
    return top_books


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