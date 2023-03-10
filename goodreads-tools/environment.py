import os


cached_friends_path = os.path.join(os.path.dirname(__file__), "cached/friends.json")
cached_compare_result_dir = os.path.join(os.path.dirname(__file__), "cached/compare_results/")


def cached_compare_result_path(user_id):
    return os.path.join(cached_compare_result_dir, f"{user_id}.json")

