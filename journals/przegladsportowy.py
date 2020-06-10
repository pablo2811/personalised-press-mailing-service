import urllib.request as u
from bs4 import BeautifulSoup as soup


def data():
    #res = "##[PRZEGLAD SPORTOWY](https://www.przegladsportowy.pl/)\n"
    res = ""
    site = u.urlopen("https://www.przegladsportowy.pl/")
    ps = soup(site,"html.parser")
    i = 0
    for art in ps.find_all("div",class_="glide__slide driverItem"):
        if i > 2:
            break
        title = art.a["data-img-alt"]
        link = art.a["href"]
        if title is not None:
            res += "* [" + title + "]" + "(" + link + ")"
            res += "\n"
            res += "\n"
            i += 1
    return res

