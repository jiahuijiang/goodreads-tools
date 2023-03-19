import os


my_id_placeholder = "MY_ID"

cached_friends_dir = os.path.join(os.path.dirname(__file__), "cached/")
cached_friends_path = os.path.join(os.path.dirname(__file__), "cached/friends.json")
cached_compare_result_dir = os.path.join(os.path.dirname(__file__), "cached/compare_results/")
cached_top_book_dir = os.path.join(os.path.dirname(__file__), "cached/top_books/")


def cached_compare_result_path(user_id):
    return os.path.join(cached_compare_result_dir, f"{user_id}.json")


def cached_top_book_path(user_id):
    return os.path.join(cached_top_book_dir, f"{user_id}.json")
