import re
import urllib.request as u
from bs4 import BeautifulSoup as soup
import os


def data():
    site = u.urlopen("https://www.onet.pl/")
    onet = soup(site, "html.parser")
    i = 0
    res = ""
    for ar in onet.find_all("article", class_="newsBox"):
        for news in ar.find_all("li"):
            if news.a is not None:
                tyt = os.linesep.join([s for s in news.a.text.splitlines() if s])
                tyt = tyt.strip()
                tyt = re.split('\n\s*\n', tyt)
                res += "* [" + tyt[-1].strip(" ") + "]" + "(" + news.a["href"] + ")"
                res += "\n"
                res += "\n"
                i += 1
            if i == 3:
                break
        if i == 3:
            break
    return res


