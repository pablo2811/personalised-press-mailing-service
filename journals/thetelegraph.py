import re
import urllib.request as u
from bs4 import BeautifulSoup as soup
import os


def data():
    site = u.urlopen("https://www.telegraph.co.uk/")
    typo = soup(site, "html.parser")
    i = 0
    res = ""
    for ar in typo.find_all("div",class_="card-labels u-order-first"):
        if ar is not None:
            tyt = os.linesep.join([s for s in ar.text.splitlines() if s])
            tyt = tyt.strip()
            tyt = re.split('\n\s*\n', tyt)
            res += "* [" + tyt[-1].strip(" ") + "]" + "(" + "https://www.telegraph.co.uk/" + ar.a["href"] + ")\n\n"
            i += 1
        if i == 3:
            break
    return res


