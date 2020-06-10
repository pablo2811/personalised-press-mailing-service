import re
import urllib.request as u
from bs4 import BeautifulSoup as soup
import os


def data():
    site = u.urlopen("https://www.tygodnikpowszechny.pl/tp-sg")
    typo = soup(site, "html.parser")
    i = 0
    #res = "##[ONET](https://www.onet.pl/)\n"
    res = ""
    x = typo.find("div",class_="views-field views-field-nothing")
    if x.a is not None:
        tyt = os.linesep.join([s for s in x.text.splitlines() if s])
        tyt = tyt.strip()
        tyt = re.split('\n\s*\n', tyt)
        res += "* [" + tyt[-1].strip(" ") + "]" + "(" + "https://www.tygodnikpowszechny.pl/tp-sg" + x.a["href"] + ")"
        res += "\n"
        res += "\n"
    for ar in typo.find_all("div", class_="views-field views-field-title"):
        if ar.a is not None:
            tyt = os.linesep.join([s for s in ar.text.splitlines() if s])
            tyt = tyt.strip()
            tyt = re.split('\n\s*\n', tyt)
            res += "* [" + tyt[-1].strip(" ") + "]" + "(" + "https://www.tygodnikpowszechny.pl/tp-sg"+ ar.a["href"] + ")"
            res += "\n"
            res += "\n"
            i += 1
        if i == 3:
            break
    return res


