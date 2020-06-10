import os
import re
import urllib.request as u
from bs4 import BeautifulSoup as soup


def data():
    site = u.urlopen("https://www.theguardian.com/international")
    guardian = soup(site, "html.parser")
    i = 1
    #res = "##[THE GUARDIAN](https://www.theguardian.com/international)\n"
    res = ""
    for art in guardian.find_all("h3",class_="fc-item__title"):
        if 6 > i > 0:
            x = art.find_all("span")[1].text
            if x:
                tyt = os.linesep.join([s for s in x.splitlines() if s])
                tyt = tyt.strip()
                tyt = re.split('\n\s*\n', tyt)
                res += "* [" + tyt[-1].strip(" ") + "]" + "(" + str(art.a["href"]) + ")"
                res += "\n"
                res += "\n"
            i += 1
            i *= -1
        else:
            i *= -1
    return res

