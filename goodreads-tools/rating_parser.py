from bs4 import PageElement


rating_by_comment = {
    "it was amazing": 5,
    "really liked it": 4,
    "liked it": 3,
    "it was ok": 2,
    "did not like it": 1
}


def get_rating_from_review(review: PageElement):
    star_rating = review.find("span", {"class": "staticStars notranslate"})
    if star_rating is not None:
        return rating_by_comment[star_rating.next_element.next_element]
    return review.next_element.stripped_strings.__next__()