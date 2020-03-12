import requests

def getGoodReadsReview(isbns):
    res = requests.get("https://www.goodreads.com/book/review_counts.json", \
        params={"key": "GOODREADS_API_KEY", "isbns": isbns})
    return res.json()
