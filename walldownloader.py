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

FLAGS = {
    '-p': 1.78,
    '-m': 0.8
}
FLAGS_DESCRIPTION = {
    '-p': 'Find wallpapers only for pc',
    '-m': 'Find wallpapers only for phones',
}

def get_images(query: str):
    data = requests.get(API_URLS['search']+f"?q={query}")
    return data.json()['data']

def get_save_id():
    return len(os.listdir(SAVE_PATH)) + 1

def get_ext(url):
    ext = os.path.splitext(url)[1]
    return ext

def save_image(image):
    data = requests.get(image['path'], stream=True)
    length = int(data.headers.get('content-length'))
    download_path = f'{SAVE_PATH}{get_save_id()}{get_ext(image["path"])}'

    with open(download_path, 'wb') as file:
        for chunk in progress.bar(data.iter_content(chunk_size=CHUNK_SIZE),
                                  expected_size=(length/CHUNK_SIZE + 1),
                                  label=f'Downloading: {image["id"]}'):
            if chunk:
                file.write(chunk)
                file.flush()

def download_images(images: list, aspect_ratio: float | None = None):
    for image in images:
        if aspect_ratio:
            if aspect_ratio - 0.2 <= float(image['ratio']) <= aspect_ratio + 0.2:
                save_image(image)
        else:
            save_image(image)



def main():
    args = arguments.Args()
    if len(args.all) == 0 or len(args.not_flags) == 0:
        print('Please specify the search query')
    else:
        if '-help' in args.flags:
            for key, value in FLAGS_DESCRIPTION.items():
                print(f"{key}:  {value}")

        query = " ".join(args.not_flags[:])
        images = get_images(query)

        if args.flags:
            if '-m' in args.flags:
                download_images(images, FLAGS['-m'])
            if '-p' in args.flags:
                download_images(images, FLAGS['-p'])
        else:
            download_images(images)


if __name__ == "__main__":
    main()
