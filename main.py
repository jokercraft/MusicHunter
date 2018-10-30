from __future__ import unicode_literals
import youtube_dl
import requests
from bs4 import BeautifulSoup
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLineEdit, QLabel
from PyQt5.QtGui import QIcon, QImage, QPalette, QBrush, QPixmap
from PyQt5.QtCore import pyqtSlot, QSize
 
class App(QWidget):
 
    def __init__(self):
        super().__init__()
        self.title = 'Music Hunter'
        self.left = 100
        self.top = 200
        self.width = 800
        self.height = 600
        self.initUI()
 
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        oImage = QImage("bg-python.jpg")
        sImage = oImage.scaled(QSize(800,600))                   # resize Image to widgets size
        palette = QPalette()
        palette.setBrush(10, QBrush(sImage))                     # 10 = Windowrole
        self.setPalette(palette)

        # Create button
        buttonSearch = QPushButton('Search', self)
        buttonSearch.setToolTip('Download the best songs of singer or band')
        buttonSearch.move(400,350)
        buttonSearch.resize(100,40) 
        buttonSearch.clicked.connect(self.search)

        buttonDownload = QPushButton('MP3', self)
        buttonDownload.setToolTip('Download as mp3')
        buttonDownload.move(400,420)
        buttonDownload.resize(100,40)  
        buttonDownload.clicked.connect(self.download)

        buttonDownload2 = QPushButton('MP4', self)
        buttonDownload2.setToolTip('Download as mp4')
        buttonDownload2.move(540,420)
        buttonDownload2.resize(100,40)  
        buttonDownload2.clicked.connect(self.download_video)

        # Create textbox
        self.textboxSearch = QLineEdit(self)
        self.textboxSearch.move(100, 350)
        self.textboxSearch.resize(280,40)
        self.textboxSearch.setPlaceholderText('Type the name of the band or signer...')

        self.textboxDownload = QLineEdit(self)
        self.textboxDownload.move(100, 420)
        self.textboxDownload.resize(280,40)
        self.textboxDownload.setPlaceholderText('Paste Youtube link of the song...')
 
        self.show()
 
    @pyqtSlot()
    def search(self):
        name = self.textboxSearch.text()
        searc_music(name)
        self.textboxSearch.setText("")
    def download(self):
        link = self.textboxDownload.text()
        download_music(link)
        self.textboxDownload.setText("")
    def download_video(self):
        link = self.textboxDownload.text()
        download_as_video(link)
        self.textboxDownload.setText("")

def download_music(link):
    try:
        ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
            }],
        }

        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                
            #ydl.download([link])
                info = ydl.extract_info(link, download=True)
        song_name = info.get('title', None)
            
    except (youtube_dl.utils.PostProcessingError,youtube_dl.utils.DownloadError):
        pass
def download_as_video(link):
    ydl_opts = {}
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([link])
            
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())



def searc_music(link):
    link = "https://www.youtube.com/results?q="
    singer_name = input("The singer or band name: ")
    link = link + singer_name
    istek = requests.get(link)
    result_html = BeautifulSoup(istek.content,"html.parser")
    result = result_html.find_all('div',{"class" : "yt-lockup yt-lockup-tile yt-lockup-video vve-check clearfix"})

    for x in result:
        d=str(x)
        d=d[94:107]
        print(d)
        try:
            ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
                }],
            }
            d=d[1:12]
            link="https://www.youtube.com/watch?v="
            link=link+d
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                
                #ydl.download([link])
                   info = ydl.extract_info(link, download=True)
            song_name = info.get('title', None)
            
        except (youtube_dl.utils.PostProcessingError,youtube_dl.utils.DownloadError):
            pass