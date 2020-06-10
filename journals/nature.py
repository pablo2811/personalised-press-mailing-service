import urllib.request as u
from bs4 import BeautifulSoup as soup


def data():
    site = u.urlopen("https://www.nature.com/")
    bi = soup(site, "html.parser")
    i = 0
    #res = "##[NATURE](https://www.nature.com/)\n"
    res = ""
    ar = bi.find("div",class_="c-hero__copy")
    res += "* [" + ar.a.text + "]" + "(" + ar.a["href"] + ")"
    res += "\n"
    res += "\n"
    for ar in bi.find_all("article", class_="u-full-height c-card c-card--flush"):
        if i == 2:
            break
        title = ar.a.text.strip(" ")
        res += "* [" + title + "]" + "(" + "https://www.nature.com"+ ar.a["href"] + ")"
        res += "\n"
        res += "\n"
        i += 1
    return res