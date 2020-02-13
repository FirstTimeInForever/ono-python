import requests
import urllib
import json
from functools import reduce
import posixpath

ARTICLES_BASE_URL = "https://api.onomedia.today/api/news/articles"
API_BASE = "https://api.onomedia.today/api"


def get_articles(category="official"):
    # url = "/".join([API_BASE, "news", "articles", category])
    url = posixpath.join(API_BASE, "news", "articles", category)
    # print(f"Using articles url: {url}")
    result = requests.get(url)
    # print("Articles get result:")
    # print(result.json())
    return result.json()


def get_articles_with_raiting():
    # url = "/".join([API_BASE, "rating_outputs"])
    url = posixpath.join(API_BASE, "rating_outputs")
    result = requests.get(url)
    data = result.json()
    if "outputs" not in data:
        raise RuntimeError("Got bad response from API!")
    # print(data["outputs"][0])
    return data["outputs"][0]


# if __name__ == "__main__":
#     print(get_articles())
#     print(get_articles_with_raiting())
