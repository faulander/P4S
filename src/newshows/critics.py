import requests
from bs4 import BeautifulSoup
import pendulum
import json
import re


def THR():
    all_articles = list()
    url = "https://www.hollywoodreporter.com/topic/tv-reviews/1"
    req = requests.get(url)
    soup = BeautifulSoup(req.text, "html.parser")

    articles = soup.find_all("article", class_="topic-card topic-card--review topic-card--media-landscape")

    for article in articles:
        title = article.find("h1", class_="topic-card__headline topic-card--landscape__headline")
        title = title.get_text()
        descr = article.find("h2", class_="topic-card__deck topic-card--landscape__deck")
        descr = descr.get_text()
        link = article.find("a", class_="topic-card__link")
        link = link['href']
        date = article.find("time", class_="topic-card__publish-time")
        date = pendulum.parse(date['datetime'])
        date = date.to_datetime_string()
        author = article.find("span", class_="topic-card__authors")
        author = author.get_text()[1:]
        source = "THR"

    article_data = {
        "title": title,
        "description": descr,
        "link": link,
        "date": date,
        "author": author,
        "source": source,
        "score1": 0,
        "score2": 0
    }
    all_articles.append(article_data)
    all_articles = json.dumps(all_articles)
    return all_articles


def METACRITIC():
    all_articles = list()
    url = "https://www.metacritic.com/browse/tv/release-date/new-series/date"
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    req = requests.get(url, headers=headers)
    soup = BeautifulSoup(req.text, "html.parser")

    articles = soup.find_all("li", class_="product season_product")

    for article in articles:
        title = article.find("a")
        link = title['href']
        link = "https://www.metacritic.com" + link
        title = title.get_text().strip()
        metascore = article.find("div", class_="metascore_w")
        try:
            metascore = int(metascore.get_text())
        except ValueError:
            metascore = 0

        userscore = article.find("li", class_="stat product_avguserscore")
        userscore = userscore.get_text().strip()
        first_digit = re.search(r"\d", userscore)
        if first_digit:
            first_digit = first_digit.start()
            userscore = userscore[first_digit:first_digit+3]
            userscore = (int(userscore[:1])*10) + int(userscore[2:])
        else:
            userscore = 0
        
        article_data = {
            "title": title,
            "description": "",
            "link": link,
            "date": pendulum.now().to_datetime_string(),
            "author": "",
            "source": "Metacritic",
            "score1": metascore,
            "score2": userscore,
        }
        all_articles.append(article_data)

    all_articles = json.dumps(all_articles)
    return all_articles

