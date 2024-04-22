from bs4 import BeautifulSoup
import requests


def get_character_prydwen(name):
    response = requests.get('https://www.prydwen.gg/star-rail/characters')

    if response.status_code == 200:
        html_content = response.content
        soup = BeautifulSoup(html_content, 'html.parser')

        pictures = soup.find_all('img')
        for picture in pictures:
            if picture['alt'].lower() == name.lower():
                pic_url = "https://www.prydwen.gg"+ picture['data-src']
                maybe_pic = requests.get(pic_url)
                if maybe_pic.status_code == 200:
                    return maybe_pic.content, name
                else:
                    print('Error loading the image:', maybe_pic.status_code)
    elif response.status_code == 500:
        print('Error loading the page:', response.status_code)
