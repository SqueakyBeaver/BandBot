import requests
from bs4 import BeautifulSoup
import pytz
import dateparser
from datetime import datetime

def get_holidays(day: str):
        date = dateparser.parse(day)
        link = f"https://www.checkiday.com/{date.month}/{date.day}/{date.year}"

        site = requests.get(link)
        soup = BeautifulSoup(site.content, "html.parser")

        holidays = soup.find(id = "masonryGrid")
        links = holidays.find_all("a")

        cnt = 0
        links_list: list[str] = []
        for i in links:
            if i.string is None:
                links_list.append(i.get('href'))

        links_list = list(set(links_list))
        cnt = 0
        for i in links_list:
            cnt += 1
            sep = i.split('/')

            if "timeanddate.com" in i:
                yield f"`[On This Day in History]({i})`"
                continue
            yield f"`[{sep[-1].replace('-', ' ').title()}]({i})`"

tz = pytz.timezone("America/Chicago")

# if datetime.now(tz).hour == 0: # I hope it works
holidays = get_holidays("today")

for i in holidays:
    print(i)
