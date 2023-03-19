import friends
import compare_results
from goodreads import get_full_url
from collaborative_filtering import predict_rating as predict_rating_with_collaborative_filtering
from top_friends import get_recommendations as get_top_friends_recommendations
import argparse


recommend_length = 10


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--verbose", action="store_true")
    parser.add_argument("--force_reload_friends", action="store_true")
    parser.add_argument("--force_reload_compare_results", action="store_true")
    parser.add_argument("--compare_algorithm", default="collaborative_filtering",
                        choices=["collaborative_filtering", "top_friends"])
    args = parser.parse_args()
    verbose = args.verbose

    all_friends = friends.get_all_friends_id(force_reload=args.force_reload_friends, verbose=verbose)
    if verbose:
        print(f"Found {len(all_friends)} friends.")

    all_friend_compare_results = compare_results.compare_with_users(
        all_friends.keys(), force_reload=args.force_reload_compare_results, verbose=verbose)
    all_books = get_all_books(all_friend_compare_results)

    if args.compare_algorithm == "top_friends":
        print("Top friends recommendation results:")
        recommendations = get_top_friends_recommendations(all_friend_compare_results, all_books, verbose=verbose)
        for book_partial_url, score, title in sorted(recommendations, key=lambda item: item[1], reverse=True)[:recommend_length]:
            if score > 0:
                print(f"{score:.1f} - {title} - {get_full_url(book_partial_url)}")

    elif args.compare_algorithm == "collaborative_filtering":
        print("Collaborative filtering recommendation results:")
        collaborative_filtering_predicted_top_similar_books = predict_rating_with_collaborative_filtering(all_friend_compare_results)
        for book_partial_url, predicted_rating in sorted(collaborative_filtering_predicted_top_similar_books.items(), key=lambda item: item[1], reverse=True)[:recommend_length]:
            if predicted_rating >= 4.0:
                print(f"{predicted_rating:.1f} - {all_books.get(book_partial_url)} - {get_full_url(book_partial_url)}")


def get_all_books(all_friend_compare_results):
    all_books = {}
    for friend_compare_result in all_friend_compare_results:
        for book in friend_compare_result.get("books_in_common"):
            all_books[book.get("partial_url")] = book.get("title")
    return all_books



if __name__ == '__main__':
    main()
