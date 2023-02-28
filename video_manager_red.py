# Created by Yuan Liu at 14:23 18/02/2023 using PyCharm
"""
Red version: does what Green version does with PyQt6 GUI
"""

import csv
import os
import re
import sys
import time

import requests
from PyQt6.QtGui import QIntValidator
from PyQt6.QtWidgets import QApplication, QLabel, QMainWindow, QPushButton, QTextEdit, QLineEdit, QWidget, \
    QGridLayout, QHBoxLayout, QVBoxLayout, QTabWidget

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


class VideoCatalogue(QMainWindow):
    def __init__(self, videos):
        super().__init__()

        self.videos = videos
        self.page_label = QLabel('Page:')
        self.page_edit = QLineEdit()
        self.page_edit.setValidator(QIntValidator(1, (len(self.videos) - 1) // 10 + 1))
        self.page_edit.returnPressed.connect(self.show_page)
        self.page_button = QPushButton('Display')
        self.page_button.clicked.connect(self.show_page)
        self.clear_button = QPushButton('Clear')
        self.clear_button.clicked.connect(self.clear_form)

        hbox = QHBoxLayout()
        hbox.addWidget(self.page_label)
        hbox.addWidget(self.page_edit)
        hbox.addWidget(self.page_button)
        hbox.addWidget(self.clear_button)

        vbox = QVBoxLayout()

        self.result_edit = QTextEdit()
        self.result_edit.setReadOnly(True)
        vbox.addWidget(self.result_edit)

        vbox.addLayout(hbox)

        central_widget = QWidget()
        central_widget.setLayout(vbox)

        self.setCentralWidget(central_widget)

    def show_page(self):
        # Ensure only a valid page be displayed.
        if not self.page_edit.text().isdigit():
            page = 1
        else:
            page = int(self.page_edit.text())
        num_pages = (len(self.videos) - 1) // 10 + 1
        page = max(1, min(page, num_pages))
        self.page_edit.setText(str(page))
        start = (page - 1) * 10
        end = start + 10

        videos = self.videos[start:end]

        text = ''
        for video in videos:
            text += f'{video[0]} {video[1]}\n'

        self.result_edit.setText(text)

    def clear_form(self):
        self.result_edit.clear()


class VideoSearch(QWidget):
    def __init__(self, videos):
        super().__init__()

        self.videos = videos
        self.search_button = QPushButton('Search')
        self.clear_button = QPushButton('Clear')
        self.id_edit = QLineEdit()
        self.text_edit = QLineEdit()
        self.result_edit = QTextEdit()
        self.result_edit.setReadOnly(True)

        grid = QGridLayout()
        grid.addWidget(QLabel('ID:'), 0, 0)
        grid.addWidget(self.id_edit, 0, 1)
        grid.addWidget(QLabel('Key Words:'), 1, 0)
        grid.addWidget(self.text_edit, 1, 1)

        hbox = QHBoxLayout()
        hbox.addWidget(self.search_button)
        hbox.addWidget(self.clear_button)

        vbox = QVBoxLayout()
        vbox.addLayout(grid)
        vbox.addWidget(self.result_edit)
        vbox.addLayout(hbox)

        self.setLayout(vbox)

        self.search_button.clicked.connect(self.search)
        self.clear_button.clicked.connect(self.clear)

    def search(self):
        id_search = self.id_edit.text()
        text_search = self.text_edit.text()

        results = []
        for video in self.videos:
            if id_search and id_search == video[0]:
                results.append(video)
            elif text_search and re.search(text_search, video[1]):
                results.append(video)

        if results:
            self.result_edit.setText('')
            for result in results:
                self.result_edit.append(f'{result[0]} {result[1]} {result[2]}')
        else:
            self.result_edit.setText('No Match Found')

    def clear(self):
        self.id_edit.setText('')
        self.text_edit.setText('')
        self.result_edit.setText('')


class VideoDownloader(QWidget):
    def __init__(self):
        super().__init__()

        self.download_button = QPushButton('Download')
        self.id_edit = QLineEdit()
        self.result_edit = QTextEdit()
        self.result_edit.setReadOnly(True)

        grid = QGridLayout()
        grid.addWidget(QLabel('ID:'), 0, 0)
        grid.addWidget(self.id_edit, 0, 1)

        vbox = QVBoxLayout()
        vbox.addLayout(grid)
        vbox.addWidget(self.result_edit)
        vbox.addWidget(self.download_button)

        self.setLayout(vbox)

        self.download_button.clicked.connect(self.download)

    def download(self):
        video_id = self.id_edit.text()

        video = None
        for v in videos:
            if v[0] == video_id:
                video = v
                break

        if video:
            filename = os.path.join(DOWNLOAD_FOLDER, f"{video[0]}-{time.strftime('%Y-%m-%d-%H-%M-%S')}.mp4")
            url = video[2]

            response = requests.get(url, stream=True)
            with open(filename, 'wb') as f:
                for chunk in response.iter_content(chunk_size=1024):
                    if chunk:
                        f.write(chunk)

            self.result_edit.setText(f'Download Completed: {os.path.abspath(filename)}')
        else:
            self.result_edit.setText('The video does NOT exist!')


def main(videos):
    app = QApplication(sys.argv)
    window = QMainWindow()
    window.setWindowTitle('Video Manager V1.2 by Yuan Liu')
    window.resize(1000, 400)  # Set the size to 800x600
    window.show()

    tab_widget = QTabWidget()

    video_catalogue = VideoCatalogue(videos)
    video_search = VideoSearch(videos)
    video_downloader = VideoDownloader()

    tab_widget.addTab(video_catalogue, 'Video Catalogue')
    tab_widget.addTab(video_search, 'Video Search')
    tab_widget.addTab(video_downloader, 'Video Download')

    window.setCentralWidget(tab_widget)
    window.show()

    sys.exit(app.exec())


if __name__ == '__main__':
    main(videos)
