import json
import os

from goodreads import Goodreads
from bs4 import BeautifulSoup
from environment import cached_compare_result_dir, cached_compare_result_path
from rating_parser import get_rating_from_review

goodreads = Goodreads()


def compare_with_users(user_ids, force_reload=False):
    print(f"Comparing with {len(user_ids)} users...")
    if not os.path.exists(cached_compare_result_dir):
        os.makedirs(cached_compare_result_dir)

    compare_results = []
    for index, user_id in enumerate(user_ids):
        print(f"Comparing with user {index + 1}/{len(user_ids)}...", end='\r')
        result_path = cached_compare_result_path(user_id)
        if force_reload is False and os.path.exists(result_path):
            print(f"Loading cached result for user {index + 1}/{len(user_ids)}...", end='\r')
            with open(result_path, 'r') as f:
                compare_results.append(json.loads(f.read()))
        else:
            compare_result = compare_with_user(user_id)
            compare_results.append(compare_result)
            with open(result_path, 'w') as f:
                f.write(json.dumps(compare_result))
    print("Comparing with users completed.")
    return compare_results


def compare_with_user(user_id):
    url = f"https://www.goodreads.com/user/compare/{user_id}"
    content = goodreads.make_request(url)

    soup = BeautifulSoup(content, 'html.parser')

    table = soup.find("table", {"class": "tableList"})

    books_in_common = []

    if table is not None:
        books = table.find_all("div", {"class": "bookBlurb"})

        for book in books:
            if book.find("a", {"class": "bookTitle"}) is not None:
                title = book.find("a", {"class": "bookTitle"}).next_element
                reviews = book.parent.parent.find_all("td")[1:]

                books_in_common.append({
                    "title": title,
                    "their_rating": get_rating_from_review(reviews[0]),
                    "my_rating": get_rating_from_review(reviews[1])
                })

    return {
        "friend_id": user_id,
        "books_in_common": books_in_common
    }
