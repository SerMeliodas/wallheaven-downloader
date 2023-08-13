import os
import sys
import pathlib
import requests
from multiprocessing import Process


PROCESSES_COUNT = 4
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

def divide_chunks(array: list, chunk_size: int):
    for i in range(0, len(array), chunk_size):
        yield array[i:i+chunk_size]

def download_images(images: list):
    for image in images:
        data = requests.get(image['path'])
        download_path = f'{SAVE_PATH}{get_save_id()}{get_ext(image["path"])}'
        open(download_path, 'wb').write(data.content)
        print(f"Downloaded:  {os.getpid()}:{image['path']}")

def create_download_processes(images: list):
    for chunk in divide_chunks(images, PROCESSES_COUNT):
        process = Process(target=download_images, args=(chunk,))
        process.start()
        process.join()

def main():
    if len(sys.argv) == 1:
        print('Please specify the search query')
    else:
        images = get_images(sys.argv[1])
        create_download_processes(images)


if __name__ == "__main__":
    main()
