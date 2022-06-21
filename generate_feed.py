# https://stackoverflow.com/a/21453238

from datetime import datetime as dt
import dateutil
from dateutil.tz import gettz
import os
from feedgen.feed import FeedGenerator
from bs4 import BeautifulSoup

# change these to reflect your project
main_url = "https://www.eviau.net/premiere"
title = "premiere"
author = {'name':'eviau', 'email':'info@eviau.net'}
href = "https://www.eviau.net/premiere"
subtitle = "RSS - premiere"
language = "en"
timezone = "America/New York"

fg = FeedGenerator()
fg.load_extension('base')

fg.id(main_url)
fg.title(title)
fg.author(author)
fg.link( href=href, rel='alternate')
fg.subtitle(subtitle)
fg.link(href=href, rel="self")
fg.language(language)

with open('./index.html') as html_text:

    soup = BeautifulSoup(html_text, 'html.parser')
    titles = soup.body.find_all("h2")
    links = soup.body.find_all("a", attrs={"class":"entry_title"})
    print(links)
    contenu = soup.body.find_all("p", attrs={"class":"entry_content"})
    times = soup.find_all("time")
    print(contenu)

    for i in range(len(links)):
        link = links[i].get_text()
        fe = fg.add_entry()
        fe.id("https://www.eviau.net/premiere/#" + link)
        fe.title(titles[i].get_text())
        fe.link(href="https://www.eviau.net/premiere/#" + link)
        fe.content(contenu[i].get_text())
        if i == 0:
            fe.updated(dt.fromtimestamp(os.path.getmtime("./index.html"),tz=gettz(timezone)))
        else:
            print(times[i].get_text())
            fe.updated(dt.fromtimestamp(dateutil.parser.isoparse(times[i].get_text()).timestamp(),tz=gettz(timezone)))
            print(fe.updated())
            
fg.atom_file('feed.xml')
