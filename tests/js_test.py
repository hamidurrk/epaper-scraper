import requests
from bs4 import BeautifulSoup

url = "https://epaper.jugantor.com/link"

data = {
    'coords': '19,117,286,374',
    'edition_id': '1',
    'ed_map_id': 'imgmap202431702046'
}

response = requests.get(url, params=data)

# print(response.url)

soup = BeautifulSoup(response.text, 'html.parser')

img_tags = soup.find('div', class_='img-ScrollBar').find_all('img')

for img_tag in img_tags:
    img_src = img_tag['src']
    print(img_src)