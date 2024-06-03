import requests
from bs4 import BeautifulSoup


def extract_news(parser):
    """ Extract news from a given web page """
    news_list = []
    news = parser.findAll("tr", class_="athing")
    for i in range(len(news)):
        item = {}
        found1 = news[i].findAll("a")[1]
        item["url"] = found1["href"]
        item["title"] = found1.string
        sibl = news[i].next_sibling.findAll("a")
        item["comments"] = int(sibl[4].string[0]) if sibl[4].string != "discuss" else 0
        item["author"] = sibl[0].string
        item["points"] = int(news[i].next_sibling.find("span", class_="score").string[0])
        news_list.append(item)
    return news_list


def extract_next_page(parser):
    """ Extract next page URL """
    next = parser.findAll("a", class_="morelink")
    return next[0]["href"]


def get_news(url, n_pages=1):
    """ Collect news from a given web page """
    news = []
    while n_pages:
        print("Collecting data from page: {}".format(url))
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        news_list = extract_news(soup)
        next_page = extract_next_page(soup)
        url = "https://news.ycombinator.com/" + next_page
        news.extend(news_list)
        n_pages -= 1
    return news
