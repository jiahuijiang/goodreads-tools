## Goodreads recommendations
Do you constantly feel unsure about what to read? Are you always not sure which friend's recommendations you should trust?\
I built this little tool to help myself find the next book to read.

## Setup
Sadly, goodreads no longer provides developer API. This tool crawls Goodreads webpages in order to 
requires you to get your username and password and set them inside your environement variable.

To use this tool:
1. Go to [Goodreads](https://www.goodreads.com/) and log in
1. Open your `networks` tab, refresh.
1. Find the request with name `www.goodreads.com`. Find `Cookie` field, get the value for key `u` and store it in an environment variable `GOODREADS_USER_ID`; get the value for key `p` and store it in an environment variable `GOODREADS_USER_PASSWORD`. This password is long live so you don't have to update it everytime you run the script.
1. Click into your profile. After it loads, you can find your user id in the full URL `https://www.goodreads.com/user/show/{uid}-{your-name}`. Store `uid` in an environment variable `GOODREADS_UID`.

## Usage
1. Clone the repository
1. Activate python virtual environment\
`source ./venv/bin/activate`
1. Run command\
There are two recommendation modes you can run in: `collabrative filtering` and `top friends`.\
`top friends` first analyzes the similiarity between you and your friends. Then get top rated books from friends that tend to rate the same books with high scores, and the lowest rated books from friends that you tend to disagree with.\
[`item-based collaborative filtering`](https://en.wikipedia.org/wiki/Collaborative_filtering) does not explicit learn similarities between users. Instead, it learns how likely certain books are rated in the same patterns, and infer what books will work for you.

## Flags
By default, the script caches the crawling results - both friend IDs and their books.\
To force reload the content, pass in `--force_reload_friends` and `force_reload_compare_results` flags into the command.\
To see intermediate outputs, e.g. your most similar friends, pass in `--verbose`.
