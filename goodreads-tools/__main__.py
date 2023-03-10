import friends
import goodreads
import os
import compare_results
import similarity_calculator


def main():
    all_friends = friends.get_all_friends_id(force_reload=True)
    print(f"Found {len(all_friends)} friends: ")

    friend_compare_results = compare_results.compare_with_users(all_friends.keys(), force_reload=False)

    friend_score = {}
    for friend_compare_result in friend_compare_results:
        similarity = similarity_calculator.calculate_similarity(friend_compare_result.get("books_in_common"))
        if similarity is not None:
            friend_score[friend_compare_result.get("friend_id")] = similarity
    print(f"Calculated similarity scores for {len(friend_score)} friends: ")

    print("Trust their recommendations")
    trust_their_likes_friends = {friend_id: scores.get("trust_their_likes")
                                 for friend_id, scores in friend_score.items()
                                 if scores.get("trust_their_likes") is not None}
    for friend_id, similarity in sorted(trust_their_likes_friends.items(), key=lambda item: item[1], reverse=True):
        print(f"{similarity} {all_friends.get(friend_id)}")
    print("Consider books they don't like")
    like_their_dislikes_friends = {friend_id: scores.get("like_their_dislikes")
                                   for friend_id, scores in friend_score.items()
                                   if scores.get("like_their_dislikes") is not None}
    if len(like_their_dislikes_friends) == 0:
        print("No friends in this category :-P")
    else:
        for friend_id, similarity in sorted(like_their_dislikes_friends.items(), key=lambda item: item[1], reverse=True):
            print(f"{similarity} {all_friends.get(friend_id)}")

if __name__ == '__main__':
    main()
