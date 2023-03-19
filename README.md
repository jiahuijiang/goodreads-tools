## Goodreads recommendations
Do you constantly feel unsure about what to read? Are you always not sure which friend's recommendations you should trust?\
I built this little tool to help myself find the next book to read.

## Setup
Sadly, goodreads no longer provides developer API. This tool crawls Goodreads webpages in order to 
requires you to get your username and password and set them inside your environement variable.
To use this tool

## Usage
1. Clone the repository
1. Activate python virtual environment\
`source ./venv/bin/activate`
1. Run command\
There are two recommendation modes you can run in: `collabrative filtering` and `top friends`.

## Others
By default, the script caches the crawling results - both friend IDs and their books. To force reload the content, pass in `--force_reload_friends` and `force_reload_compare_results` flags into the command.
