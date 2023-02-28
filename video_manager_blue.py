# Created by Yuan Liu at 06:31 18/02/2023 using PyCharm
"""
Blue version: does what Green version does and also:
    - Support multiple videos download by passing a list;
    - Use a proper progress bar from tqdm library;
    - Apply multi-threading to speed up the download
"""

import csv
import os
import re
import time
from multiprocessing.pool import ThreadPool

import requests
from tqdm import tqdm

VIDEO_FILE = 'video.csv'
DOWNLOAD_FOLDER = 'files'

# Get video info from the file
videos = []
with open(VIDEO_FILE, 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    for row in reader:
        # Fix the wrong comma used in the mid of the news title
        if len(row) > 3:
            row[1:3] = ['，'.join(row[1:3])]
        videos.append(row)


def get_dest_path(download_folder: str = "downloads", file_name: str = "my_video.mp4"):
    """
    Get the destination path to save videos.
    """

    # Define the download folder
    download_path = os.path.join(os.getcwd(), download_folder)

    # Create the download folder if it doesn't exist
    if not os.path.exists(download_path):
        os.mkdir(download_path)

    # Set the destination path for the file
    destination_path = os.path.join(download_path, file_name)

    return destination_path


def display_videos(page_num: int = 1, items_per_page: int = 10):
    """
    Display items by page and show Page 1 if the page_num is invalid.
    """
    exact_page = len(videos) / items_per_page
    total_page = int(exact_page) + (float(exact_page) > int(exact_page))
    if page_num < 0 or page_num > total_page:
        print("Invalid page number! Will display Page 1 instead:")
        page_num = 1

    print(f"Displaying Page {page_num} below:")
    start_index = (page_num - 1) * items_per_page
    end_index = start_index + items_per_page
    for video in videos[start_index:end_index]:
        print(', '.join(video))


def search_videos(search_pattern):
    """
    Find videos whose names match the search pattern.
    """
    for video in videos:
        if re.search(search_pattern, video[1], re.IGNORECASE):
            print(', '.join(video))


def download_video(video_id, pbar):
    """
    Download the desired video and save it to the destination folder.
    """
    # Find video info for given ID
    video_info = None
    for video in videos:
        if video[0] == video_id:
            video_info = video
            break
    if not video_info:
        print('Video ID NOT found!')
        return

    # Construct filename and download path
    file_name = f"{video_id}-{time.strftime('%Y-%m-%d-%H-%M-%S')}.mp4"
    download_path = get_dest_path(DOWNLOAD_FOLDER, file_name)

    # Download video and display progress
    url = video_info[2]
    res = requests.get(url, stream=True)
    pbar.set_description(f"Downloading {file_name}")
    with open(download_path, 'wb') as f:
        pbar.update()
        for chunk in res.iter_content(128):
            f.write(chunk)


def download_videos(video_ids: list, threads_num: int = 8):
    """
    Download the specified videos using multi-threads.
    """
    # Reset threads number when number of videos is less than that of threads
    if threads_num < len(list(video_ids)):
        threads_num = min(threads_num, len(list(video_ids)))

    # Set up multi-thread to download multiple videos faster.
    with ThreadPool(processes=threads_num) as pool:
        # Create a progress bar for total number of threads
        with tqdm(desc=f"Downloading videos...", total=len(video_ids),
                  bar_format= '{l_bar}{bar:10}{r_bar}|Total Time: {elapsed}', ncols = 200) as pbar:
            pool.starmap(download_video, [(video_id, pbar) for video_id in video_ids])


def main():
    """
    Run the video manager.
    """
    while True:
        choice = input("Select an option: 1) View Page, 2) Search Videos, 3) Download Video, q) Quit\n")
        if choice == '1':
            page_num = int(input("Enter page number: "))
            display_videos(page_num, items_per_page=10)
        elif choice == '2':
            search_str = input("Enter search string: ")
            search_videos(search_str)
        elif choice == '3':
            video_ids_str = input("Enter video IDs (separated by ','): ")
            video_ids = list(set([v.strip() for v in video_ids_str.split(',')]))
            download_videos(video_ids)
        elif choice.lower() == 'q':
            break
        else:
            print("Invalid choice")


if __name__ == '__main__':
    main()
