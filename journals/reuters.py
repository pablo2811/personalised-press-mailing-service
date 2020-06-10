import re
import urllib.request as u
from bs4 import BeautifulSoup as soup
import os

def data():
    #res = "##[REUTERS](https://www.reuters.com/)\n"
    res = ""
    site = u.urlopen("https://www.reuters.com/")
    ps = soup(site,"html.parser")
    i = 0
    for art in ps.find_all("div",class_="story-content"):
        if i > 3:
            break
        if i > 0:
            title = art.text
            link = art.a["href"]
            tyt = os.linesep.join([s for s in title.splitlines() if s])
            tyt = tyt.strip()
            tyt = re.split('\n\s*\n', tyt)
            res += "* [" + tyt[-1].strip(" ") + "]" + "(" + "https://www.reuters.com" + link + ")"
            res += "\n"
            res += "\n"
        i += 1
    return res

