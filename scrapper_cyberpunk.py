from bs4 import BeautifulSoup
import requests
from datetime import date
import pandas as pd

LAST_PAGE = 68


urls = ['https://www.jeuxvideo.com/jeux/pc/jeu-45155/avis/'+'?p='+str(nb_page) for nb_page in range(1,LAST_PAGE+1)]

reviews = []
ratings = []
dates = []

for url in urls:
    
    html = requests.get(url).content
    soup = BeautifulSoup(html, 'html.parser')

    for block_avis in soup.select('div.bloc-avis-tous.px-3.px-lg-0'):
        
        for tag_review in block_avis.select('div.txt-avis.text-enrichi-forum'):
            reviews.append(tag_review.get_text().strip())

        for tag_rating in block_avis.select('div.note-avis strong'):
            ratings.append(tag_rating.get_text())

        for tag_date in block_avis.select('div.bloc-date-avis'):
            dates.append(tag_date.get_text().strip())

data = pd.DataFrame(list(zip(reviews,ratings,dates)), columns=["review","rating","date"])
data.rating = data.rating.astype(int)

data.to_csv(f'scrapped_cyberpunk_{str(date.today())}.csv', index=False)

