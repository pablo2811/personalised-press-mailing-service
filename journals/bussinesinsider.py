import urllib.request as u
from bs4 import BeautifulSoup as soup


def data():
    site = u.urlopen("https://businessinsider.com.pl/")
    bi = soup(site, "html.parser")
    i = 0
    #res = "##[BUSSINES INSIDER](https://businessinsider.com.pl/)\n"
    res = ""
    for ar in bi.find_all("article"):
        if ar is not None and ar.a is not None and i != 0:
            res += "* [" + str(ar.a.text) + "]" + "(" + ar.a["href"] + ")"
            res += "\n"
            res += "\n"
        if i > 4:
            break
        i += 1
    return res