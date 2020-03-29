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

def GUARDIAN():
    all_articles = list()
    url = "https://www.theguardian.com/tv-and-radio/series/tv-review"
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    req = requests.get(url, headers=headers)
    soup = BeautifulSoup(req.text, "html.parser")

    articles = soup.find_all("section", class_="fc-container fc-container--tag")

    for article in articles:
        tmp_title = article.find("a", class_="u-faux-block-link__overlay js-headline-text")
        link = tmp_title['href']
        tmp_title = tmp_title.get_text()
        pos_review = tmp_title.find("review")
        if pos_review > 0:
            tmp_title = tmp_title[:pos_review-1]
        title = tmp_title
        tmp_descr = article.find("div", class_="fc-item__standfirst")
        try:
            tmp_descr = tmp_descr.get_text()
            descr = tmp_descr.strip()
        except AttributeError:
            descr = ""

        date = article.find("time", class_="fc-date-headline")
        date = pendulum.parse(date['datetime'])
        date = date.to_datetime_string()

        score1 = article.find("span", class_="u-h")
        score1 = score1.get_text()
        pos_of = score1.find("out")
        if pos_of > 0:
            score1 = (int(score1[:pos_of-1]))*20
        else:
            score1 = 0

        article_data = {
            "title": title,
            "description": descr,
            "link": link,
            "date": date,
            "author": "",
            "source": "GUARDIAN",
            "score1": score1,
            "score2": 0,
        }
        all_articles.append(article_data)

    all_articles = json.dumps(all_articles)
    return all_articles

def SJ():
    pendulum.set_locale('de')
    all_articles = list()
    url = "https://www.serienjunkies.de/thema/pilot-reviews/"
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    req = requests.get(url, headers=headers)
    req.encoding = 'utf-8'
    soup = BeautifulSoup(req.text, "html.parser")

    articles = soup.find_all("div", class_="fixit bottomabstand e1")

    for article in articles:
        title = article.find("h3").get_text()
        pos_addon = title.find("Review")
        if pos_addon > 0:
            title = title[:pos_addon]
        title = title.strip()
        if title[-1] == ":" or title[-1] == "-":
            title = title[:len(title)-1]
        link = "https://www.serienjunkies.de" + article.find("a")["href"]
        descr = article.find("p").get_text()

        fullstars = len(article.find_all("i", class_="fa fa-star goldstar"))
        halfstars = len(article.find_all("i", class_="fa fa-star-half-o goldstar"))

        score1 = fullstars * 20
        if halfstars:
            score1 += 10    

        date = article.find("div", class_="clear sgml").get_text()
        pos_de = date.find(", den ") #6
        pos_von = date.find(" von ") #5   
        date = (date[pos_de+6:pos_von-4]).strip()
        date = (pendulum.from_format(date, "DD. MMMM YYYY HH.mm")).to_datetime_string()
        

        article_data = {
            "title": title,
            "description": descr,
            "link": link,
            "date": date,
            "author": "",
            "source": "SJ.de",
            "score1": score1,
            "score2": 0,
        }
        all_articles.append(article_data)
    all_articles = json.dumps(all_articles)
    pendulum.set_locale('en')
    return all_articles

