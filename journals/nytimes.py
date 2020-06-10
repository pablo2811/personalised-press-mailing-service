import urllib.request as u
from bs4 import BeautifulSoup as soup


def data():
    #res = "##[NY TIMES](https://www.nytimes.com/)\n"
    res = ""
    site = u.urlopen("https://www.nytimes.com/")
    nytimes = soup(site,"html.parser")
    i = 0
    for art in nytimes.find_all("div",class_="css-6p6lnl"):
        link = "https://www.nytimes.com/" + art.a["href"]
        obj = art.a.h2.span
        if i > 2:
            break
        if obj is not None:
            title = art.a.h2.span.text
            res += "* [" + title + "]" + "(" + link + ")"
            res += "\n"
            res += "\n"
            i += 1

    return res


