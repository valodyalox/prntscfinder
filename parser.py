import requests
import os
import re
from datetime import datetime
from bs4 import BeautifulSoup as bs
import random
import logging

domain = "https://prnt.sc/"
path = "files\\"

log = logging.getLogger("Log")
log.setLevel(logging.DEBUG)
fh = logging.FileHandler(f"log.log")
formatter = logging.Formatter("%(levelname)s %(asctime)s: %(message)s", "%d.%m.%Y %H:%M:%S")
fh.setFormatter(formatter)
log.addHandler(fh)

log.debug("RUNNING APPLICATION\n\n")

headers = {
    "user-agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:21.0) Gecko/20130331 Firefox/21.0"
}

symbols = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0", 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k',
           'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

empty_urls = []


def isExistOnPC(name, path):
    if os.path.exists(path + name):
        return True
    else:
        return False


def getImageFormat(url):
    return re.split(".", url[-6:], 1)[1]


def DownloadImage(url, name, path, i):
    if not isExistOnPC(name, path):
        print(f"Downloading: {url} from {domain}{name}..")
        try:
            with open(f"{path}{i} {name}{getImageFormat(url)}", "wb") as file:
                image = requests.get(url, headers=headers)
                file.write(image.content)

        except Exception as error:
            log.error(f"Couldn't download {domain}{name}, {error}")
            return os.remove(f"{path}{name}{getImageFormat(url)}")

        else:
            log.info(f"Downloaded {domain}{name}")


def FindPictures(domain, sybmols, i):
    name = "".join(random.choice(sybmols) for _ in range(6))
    while name[0] == 0:
        print(f"reformatting {name} to ", end="")
        name[0] = random.choice(sybmols)
        print(name)

    url = domain + name

    # url = "https://prnt.sc/g5o5n8" NONE EXAMPLE
    ans = requests.get(url, headers=headers)

    soup = bs(ans.content, "lxml")

    if soup.find("img", {"id": "screenshot-image", "class": "no-click screenshot-image",
                         "src": "//st.prntscr.com/2020/08/01/0537/img/0_173a7b_211be8ff.png"}) is not None and url not in empty_urls:
        print(f"{url} not contain image")
        log.warning(f"{url} not contain image")
        empty_urls.append(url)
    else:
        for img in soup.find_all("img", {"id": "screenshot-image", "class": "no-click screenshot-image"}):
            DownloadImage(img["src"], name, path, i)


i = 1
while True:
    try:
        print(f"({i}) ", end="")
        FindPictures(domain, symbols, i)
        i = i + 1
    except KeyboardInterrupt:
        break

print("\nРабота заверщена")