import os
import pathlib
import requests
from clint import arguments
from clint.textui import progress


CHUNK_SIZE = 1024
SAVE_PATH = f'{pathlib.Path.home()}/Pictures/wallpapers/'
API_URLS = {
    'search' : 'https://wallhaven.cc/api/v1/search',
}


def get_images(query: str):
    data = requests.get(API_URLS['search']+f"?q={query}")
    return data.json()['data']

def get_save_id():
    return len(os.listdir(SAVE_PATH))

def get_ext(url):
    ext = os.path.splitext(url)[1]
    return ext

def download_images(images: list):
    for image in images:

        data = requests.get(image['path'], stream=True)
        download_path = f'{SAVE_PATH}{get_save_id()}{get_ext(image["path"])}'
        length = int(data.headers.get('content-length'))

        with open(download_path, 'wb') as file:

            for chunk in progress.bar(data.iter_content(chunk_size=CHUNK_SIZE),
                                      expected_size=length/CHUNK_SIZE + 1,
                                      label=f'Downloading: {image["id"]}'):
                if chunk:
                    file.write(chunk)
                    file.flush()

def main():
    args = arguments.Args()
    if len(args.all) == 0:
        print('Please specify the search query')
    else:
        images = get_images(args.get(0))
        download_images(images)


if __name__ == "__main__":
    main()
