import os
from pathlib import Path

from parsel import Selector
import requests

BASE_DIR = Path(__file__).resolve().parent

def main(query: str, max_page: int = 5):
    base_url = 'https://prcm.jp/list/' + query
    for page in range(1, max_page + 1):
        url = base_url + f'?page={page}'
        response = requests.get(url)
        selector = Selector(response.text)
        for anchor in selector.css('.list-pic.list-pic--is-3col li a'):
            detail_url = anchor.attrib.get('href')
            response = requests.get(detail_url)
            selector = Selector(response.text)
            image_url = selector.css('a.pic-img img').attrib.get('src')
            image_filename = os.path.basename(image_url)
            image_response = requests.get(image_url, stream=True)
            path = BASE_DIR / 'images/input' / image_filename
            print(str(path))
            with open(path, 'wb') as f:
                f.write(image_response.content)


if __name__ == '__main__':
    query = '中丸'
    main(query)
