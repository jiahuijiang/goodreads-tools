import math

from get_friend_books import get_friends_top_books
import similarity_calculator


def get_recommendations(all_friend_compare_results, all_friends, verbose=False):
    friend_score = calculate_similarity_into_score(all_friend_compare_results)

    similarity_in_likes_of_relevant_friends = calculate_similarity_in_likes(friend_score, all_friends)
    similarity_in_dislikes_of_relevant_friends = calculate_similarity_in_dislikes(friend_score, all_friends)

    all_relevant_friends = \
        set(similarity_in_likes_of_relevant_friends.keys()) | set(similarity_in_dislikes_of_relevant_friends.keys())
    friend_top_books = get_friends_top_books(all_relevant_friends, force_reload=False)

    return compute_recommendations(friend_top_books, similarity_in_likes_of_relevant_friends, similarity_in_dislikes_of_relevant_friends)


def calculate_similarity_into_score(friend_compare_results, verbose=False):
    friend_score = {}
    for friend_compare_result in friend_compare_results:
        similarity = similarity_calculator.calculate_similarity(friend_compare_result.get("books_in_common"))
        if similarity is not None:
            friend_score[friend_compare_result.get("friend_id")] = similarity
    if verbose:
        print(f"Calculated similarity scores for {len(friend_score)} friends.\n")
    return friend_score


def calculate_similarity_in_likes(friend_score, all_friends, verbose=False):
    if verbose:
        print("Trust their recommendations:")
    similarity_in_likes = {friend_id: scores.get("trust_their_likes")
                                 for friend_id, scores in friend_score.items()
                                 if scores.get("trust_their_likes") is not None}
    if verbose:
        for friend_id, similarity in sorted(similarity_in_likes.items(), key=lambda item: item[1], reverse=True):
            print(f"{similarity} {all_friends.get(friend_id)}"
                  f" - {friend_score.get(friend_id).get('trust_their_likes_count')} books")
    return similarity_in_likes


def calculate_similarity_in_dislikes(friend_score, all_friends, verbose=False):
    if verbose:
        print("\nConsider books they don't like:")
    dissimilarity_in_dislikes = {friend_id: scores.get("like_their_dislikes")
                                 for friend_id, scores in friend_score.items()
                                 if scores.get("like_their_dislikes") is not None}
    if verbose:
        if len(dissimilarity_in_dislikes) == 0:
            print("No friends in this category :-P")
        else:
            for friend_id, similarity in sorted(dissimilarity_in_dislikes.items(), key=lambda item: item[1], reverse=True):
                print(f"{similarity} {all_friends.get(friend_id)}"
                      f" - {friend_score.get(friend_id).get('like_their_dislikes_count')} books")
    return dissimilarity_in_dislikes


def compute_recommendations(friend_top_books, similarity_in_likes_of_relevant_friends, similarity_in_dislikes_of_relevant_friends):
    # base score from similarity-in-likes friends:
    #   each 5-star rating: 2 points, each 4-star rating: 1 point
    #   weighted by similarity score, and divided by sqrt of sum of similarity scores
    # base score from similarity-in-dislikes friends:
    #   each 1-star rating: 2 points, each 2-star rating: 1 point
    #   weighted by similarity score, and divided by sqrt of sum of similarity scores
    book_titles = {}

    score_from_likes = {}
    sum_of_similarity_in_likes = {}
    for friend_id, similarity in similarity_in_likes_of_relevant_friends.items():
        top_books = friend_top_books.get(friend_id)
        for book in top_books:
            book_partial_url = book.get("partial_url")
            rating = book.get("rating")
            if type(rating) is int and rating >= 4:
                score_from_likes[book_partial_url] = score_from_likes.get(book_partial_url, 0.0) + similarity * (rating - 3)
                sum_of_similarity_in_likes[book_partial_url] = sum_of_similarity_in_likes.get(book_partial_url, 0.0) + similarity
                book_titles[book_partial_url] = book.get("title")

    score_from_dislikes = {}
    sum_of_similarity_in_dislikes = {}
    for friend_id, similarity in similarity_in_dislikes_of_relevant_friends.items():
        top_books = friend_top_books.get(friend_id)
        for book in top_books:
            book_partial_url = book.get("partial_url")
            rating = book.get("rating")
            if type(rating) is int and rating <= 2:
                score_from_dislikes[book_partial_url] = score_from_dislikes.get(book_partial_url, 0.0) + similarity * (3 - rating)
                sum_of_similarity_in_dislikes[book_partial_url] = sum_of_similarity_in_dislikes.get(book_partial_url, 0.0) + similarity
                book_titles[book_partial_url] = book.get("title")

    # final score = base score from likes + base score from dislikes
    recommendations = []
    for book_id in set(score_from_likes.keys()) | set(score_from_dislikes.keys()):
        score = 0.0
        if sum_of_similarity_in_likes.get(book_id, 0.0) > 0:
            score += score_from_likes.get(book_id, 0.0) / math.sqrt(sum_of_similarity_in_likes.get(book_id, 0.0))
        if sum_of_similarity_in_dislikes.get(book_id, 0.0) > 0:
            score += score_from_dislikes.get(book_id, 0.0) / math.sqrt(sum_of_similarity_in_dislikes.get(book_id, 0.0))
        recommendations.append((book_id, score, book_titles.get(book_id)))

    return recommendations
