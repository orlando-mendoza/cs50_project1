import requests
from application import app


def get_good_reads_review(isbn):
    res = requests.get("https://www.goodreads.com/book/review_counts.json",
                       params={"key": app.config.get("API_KEY"), "isbns": isbn})
    return res.json()


def get_book_cover(isbn):
    res = requests.get("https://www.googleapis.com/books/v1/volumes?q=isbn:" + isbn)
    if res.json()['totalItems'] != 0:
        return res.json()['items'][0]['volumeInfo']['imageLinks']['thumbnail']
    else:
        return "NO Cover FOUND"
