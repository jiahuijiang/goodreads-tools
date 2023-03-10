# for each book
# if the rating is similar (1 point apart), score +1
# if the rating is different, score -(difference-1)
def calculate_similarity(books_in_common):
    similarity = 0
    books_both_read = 0
    counted = 0

    def both_love(book):
        return book["their_rating"] >= 4 and book["my_rating"] >= 4

    def disapprove_their_high_rating(book):
        return book["their_rating"] >= 4 and abs(book["their_rating"] - book["my_rating"]) >= 2

    def is_their_dislike(book):
        return book["their_rating"] <= 2

    def like_the_book(book):
        return book["my_rating"] >= 4

    trust_their_likes_scores = 0
    their_liked_book_count = 0

    like_their_dislikes = 0
    their_disliked_book_count = 0
    for book_in_common in books_in_common:
        # only books that both people have ratings contribute to similarity
        if type(book_in_common["their_rating"]) is int and type(book_in_common["my_rating"]) is int:
            if both_love(book_in_common):
                trust_their_likes_scores = trust_their_likes_scores + 1
                their_liked_book_count = their_liked_book_count + 1
            elif disapprove_their_high_rating(book_in_common):
                trust_their_likes_scores = trust_their_likes_scores - 2
                their_liked_book_count = their_liked_book_count + 1
            elif is_their_dislike(book_in_common):
                their_disliked_book_count = their_disliked_book_count + 1
                if like_the_book(book_in_common):
                    like_their_dislikes = like_their_dislikes + 1

    return {
        "trust_their_likes": trust_their_likes_scores / their_liked_book_count if their_liked_book_count >= 5 else None,
        "like_their_dislikes": like_their_dislikes / their_disliked_book_count if their_disliked_book_count >= 3 else None
    }
