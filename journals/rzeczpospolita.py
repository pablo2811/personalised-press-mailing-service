import re
import urllib.request as u
from bs4 import BeautifulSoup as soup
import os


def data():
    site = u.urlopen("https://www.rp.pl/")
    typo = soup(site, "html.parser")
    i = 0
    res = ""
    x = typo.find("h2",class_="main-topic__title")
    if x is not None:
        tyt = os.linesep.join([s for s in x.text.splitlines() if s])
        tyt = tyt.strip()
        tyt = re.split('\n\s*\n', tyt)
        res += "* [" + tyt[-1].strip(" ") + "]" + "(" + x.parent["href"] + ")"
        res += "\n"
        res += "\n"

    for ar in typo.find_all("h3",class_="teaser__title"):
        if ar is not None:
            tyt = os.linesep.join([s for s in ar.text.splitlines() if s])
            tyt = tyt.strip()
            tyt = re.split('\n\s*\n', tyt)
            res += "* [" + tyt[-1].strip(" ") + "]" + "(" + ar.parent["href"] + ")"
            res += "\n"
            res += "\n"
            i += 1
        if i == 3:
            break
    return res


