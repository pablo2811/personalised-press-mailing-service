import urllib.request as u
from bs4 import BeautifulSoup as soup


def data():
    site = u.urlopen("https://www.economist.com/")
    bi = soup(site, "html.parser")
    i = 0
    #res = "##[THE ECONOMIST](https://www.economist.com/)\n"
    res = ""
    for ar in bi.find_all("a",class_="headline-link"):
        res += "* [" + str(ar.text) + "]" + "(" + "https://www.economist.com"+ ar["href"] + ")"
        res += "\n"
        res += "\n"
        if i == 2:
            break
        i += 1
    return res
