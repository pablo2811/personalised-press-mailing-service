import re
import urllib.request as u
from bs4 import BeautifulSoup as soup
import os

def data():
    #res = "##[WASHINGTON POST OPINION](https://www.washingtonpost.com//)\n"
    res = ""
    site = u.urlopen("https://www.washingtonpost.com/")
    ps = soup(site,"html.parser")
    i = 0
    for art in ps.find_all("div",class_="headline xx-small thin-style text-align-inherit"):
        if i > 2:
            break
        title = art.text
        link = art.a["href"]
        tyt = os.linesep.join([s for s in title.splitlines() if s])
        tyt = tyt.strip()
        tyt = re.split('\n\s*\n', tyt)
        res += "* [" + tyt[-1].strip(" ") + "]" + "(" + link + ")"
        res += "\n"
        res += "\n"
        i += 1
    return res


