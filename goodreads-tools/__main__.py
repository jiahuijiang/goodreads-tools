import friends
import goodreads
import os
import compare_results
import similarity_calculator
from get_top_books import get_friends_top_books


def main():
    all_friends = friends.get_all_friends_id(force_reload=False)
    print(f"Found {len(all_friends)} friends.")

    friend_compare_results = compare_results.compare_with_users(all_friends.keys(), force_reload=False)
    friend_score = calculate_similarity_into_score(friend_compare_results)

    similarity_in_likes_of_relevant_friends = calculate_similarity_in_likes(friend_score, all_friends)
    similarity_in_dislikes_of_relevant_friends = calculate_similarity_in_dislikes(friend_score, all_friends)

    all_relevant_friends = \
        set(similarity_in_likes_of_relevant_friends.keys()) | set(similarity_in_dislikes_of_relevant_friends.keys())
    friend_top_books = get_friends_top_books(all_relevant_friends, force_reload=False)

    compute_recommendations(friend_top_books, similarity_in_likes_of_relevant_friends)


def calculate_similarity_into_score(friend_compare_results):
    friend_score = {}
    for friend_compare_result in friend_compare_results:
        similarity = similarity_calculator.calculate_similarity(friend_compare_result.get("books_in_common"))
        if similarity is not None:
            friend_score[friend_compare_result.get("friend_id")] = similarity
    print(f"Calculated similarity scores for {len(friend_score)} friends.\n")
    return friend_score


def calculate_similarity_in_likes(friend_score, all_friends):
    print("Trust their recommendations:")
    similarity_in_likes = {friend_id: scores.get("trust_their_likes")
                                 for friend_id, scores in friend_score.items()
                                 if scores.get("trust_their_likes") is not None}
    for friend_id, similarity in sorted(similarity_in_likes.items(), key=lambda item: item[1], reverse=True):
        print(f"{similarity} {all_friends.get(friend_id)}"
              f" - {friend_score.get(friend_id).get('trust_their_likes_count')} books")
    return similarity_in_likes


def calculate_similarity_in_dislikes(friend_score, all_friends):
    print("\nConsider books they don't like:")
    dissimilarity_in_dislikes = {friend_id: scores.get("like_their_dislikes")
                                 for friend_id, scores in friend_score.items()
                                 if scores.get("like_their_dislikes") is not None}
    if len(dissimilarity_in_dislikes) == 0:
        print("No friends in this category :-P")
    else:
        for friend_id, similarity in sorted(dissimilarity_in_dislikes.items(), key=lambda item: item[1], reverse=True):
            print(f"{similarity} {all_friends.get(friend_id)}"
                  f" - {friend_score.get(friend_id).get('like_their_dislikes_count')} books")
    return dissimilarity_in_dislikes


if __name__ == '__main__':
    main()
