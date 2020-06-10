import re
import urllib.request as u
from bs4 import BeautifulSoup as soup
import os

def data():
    site = u.urlopen("https://www.ft.com/")
    typo = soup(site, "html.parser")
    i = 0
    res = ""
    for ar in typo.find_all("div", class_="o-teaser__heading"):
        if ar.a is not None:
            tyt = os.linesep.join([s for s in ar.text.splitlines() if s])
            tyt = tyt.strip()
            tyt = re.split('\n\s*\n', tyt)
            res += "* [" + tyt[-1].strip(" ") + "]" + "(" + "https://www.ft.com" + ar.a["href"] + ")"
            res += "\n"
            res += "\n"
            i += 1
        if i == 3:
            break
    return res
