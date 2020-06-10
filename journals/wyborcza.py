import urllib.request as u
from bs4 import BeautifulSoup as soup


def data():
    #res = "##[GAZETA WYBORCZA](https://wyborcza.pl/0,0.html)\n"
    res = ""
    site = u.urlopen("https://wyborcza.pl/0,0.html")
    wyborcza = soup(site,"html.parser")
    for art in wyborcza.find_all("div",class_="mod-generic-subitem-title"):
        res += "* [" + str(art.a.text) + "]" + "(" + str(art.a["href"]) + ")"
        res += "\n"
        res += "\n"
    return res

