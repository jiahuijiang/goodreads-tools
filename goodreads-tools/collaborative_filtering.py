from sklearn.neighbors import NearestNeighbors
from environment import my_id_placeholder
import pandas as pd
from get_friend_books import get_friends_top_books, get_my_top_books
from goodreads import get_my_id

number_neighbors = 10


# friend_compare_results is a list of dicts
# each dict has the following keys:
#   friend_id
#   books_in_common:
#       list of dicts, each dict has the following keys:
#           partial_url, title, their_rating, my_rating
def predict_rating(all_friend_compare_results, force_reload=False, verbose=False):
    all_friends = [compare_result.get("friend_id") for compare_result in all_friend_compare_results]
    all_books_from_compare = get_all_rated_books_from_compare(all_friend_compare_results)

    friends_top_books = get_friends_top_books(all_friends, force_reload, verbose)
    all_books_from_top_books = get_all_rated_books_from_top_books(friends_top_books)

    my_id = get_my_id()
    my_top_books = get_my_top_books(force_reload, verbose)
    all_books_from_my_top_books = get_all_rated_books_from_top_books({my_id: my_top_books})

    all_books = {**all_books_from_compare, **all_books_from_top_books, **all_books_from_my_top_books}
    all_book_urls = all_books.keys()

    score_df = pd.DataFrame(index=all_book_urls, columns=[my_id_placeholder, *all_friends])
    score_df.fillna(0, inplace=True)

    for friend_compare_result in all_friend_compare_results:
        friend_id = friend_compare_result.get("friend_id")
        for book in friend_compare_result.get("books_in_common"):
            if type(book.get("my_rating")) is int and book.get("my_rating") > 0:
                score_df.at[book.get("partial_url"), my_id_placeholder] = book.get("my_rating")
            if type(book.get("their_rating")) is int and book.get("their_rating") > 0:
                score_df.at[book.get("partial_url"), friend_id] = book.get("their_rating")

    for friend_id, friend_top_books in friends_top_books.items():
        for book in friend_top_books:
            if book.get("rating") > 0:
                score_df.at[book.get("partial_url"), friend_id] = book.get("rating")

    for book in my_top_books:
        if book.get("rating") > 0:
            score_df.at[book.get("partial_url"), my_id_placeholder] = book.get("rating")

    knn = NearestNeighbors(metric='cosine', algorithm='brute')
    knn.fit(score_df.values)
    distances, indices = knn.kneighbors(score_df.values, n_neighbors=number_neighbors)

    predicted_ratings = []

    for book_index, book_partial_url in list(enumerate(score_df.index)):
        # for every book that I haven't rated
        if score_df.iloc[book_index, 0] == 0:
            # get the similar books
            similar_books_indices = indices[book_index].tolist()
            similar_book_distances = distances[book_index].tolist()

            # prediction for rating of book_index can be calculated through my ratings of similar books
            # weighted by the similarity of the book to the book_index
            total_weighted_score = 0.0
            denominator = 0.0
            for local_index, similar_book_global_index in enumerate(similar_books_indices):
                # for every similar book that I have rated
                if similar_book_global_index != book_index and score_df.iloc[similar_book_global_index, 0] != 0:
                    similarity = 1.0 - similar_book_distances[local_index]
                    total_weighted_score += similarity * score_df.iloc[similar_book_global_index, 0]
                    denominator += similarity

            if denominator != 0:
                predicted_ratings.append({
                    "partial_url": book_partial_url,
                    "title": all_books.get(book_partial_url),
                    "predicted_rating": total_weighted_score / denominator
                })

    return predicted_ratings


def get_all_rated_books_from_compare(all_friend_compare_results):
    all_books = {}
    for friend_compare_result in all_friend_compare_results:
        for book in friend_compare_result.get("books_in_common"):
            if type(book.get("their_rating")) is int or type(book.get("my_rating")) is int:
                all_books[book.get("partial_url")] = book.get("title")
    return all_books


def get_all_rated_books_from_top_books(friends_top_books):
    all_books = {}
    for friend_id, friend_top_books in friends_top_books.items():
        for book in friend_top_books:
            if type(book.get("rating")) is int:
                all_books[book.get("partial_url")] = book.get("title")
    return all_books


def get_all_rated_books_urls(all_friend_compare_results):
    all_rated_books_urls = set()
    for friend_compare_result in all_friend_compare_results:
        for book in friend_compare_result.get("books_in_common"):
            if type(book.get("my_rating")) is int or type(book.get("their_rating")) is int:
                all_rated_books_urls.add(book.get("partial_url"))
    return list(all_rated_books_urls)
