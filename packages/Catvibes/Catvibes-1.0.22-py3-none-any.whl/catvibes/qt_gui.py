from PyQt6.QtWidgets import (
    QApplication,
    QProgressBar,
    QPushButton,
    QMainWindow,
    QScrollArea,
    QVBoxLayout,
    QWidget,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QTabWidget,
    QLineEdit,
    QCompleter,
    QMenu, QLayout,
    QStyleFactory,
    QStyle,
    QDialog,
    QComboBox
)

from PyQt6.QtGui import (
    QAction,
    QColor,
    QPalette,
    QPixmap,
    QImage,
    QStandardItemModel, QStandardItem, QCursor, QIcon
)

from PyQt6.QtCore import (
    QTimer,
    Qt, QSize,
    QThread,
    pyqtSignal
)


import sys
from pathlib import Path
from functools import partial
import eyed3
import requests
import logging

from catvibes.catvibes_lib import hash_container

try:
    from catvibes import catvibes_lib as lib
except ModuleNotFoundError:
    import catvibes_lib as lib

playlists = lib.playlists
song_data = lib.song_data


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Catvibes")
        layout = QGridLayout()
        layout.setContentsMargins(0, 0, 0, 0)

        global player
        player = PlayerWidget()
        lib.music_player = player
        layout.addWidget(player, 0, 1)

        playlists_widget = QTabWidget()

        new_playlist = QWidget()

        def on_tab_change():
            if playlists_widget.currentWidget() != new_playlist:
                playlists_widget.currentWidget().refresh()
            else:
                dialog = NewPlaylistDialog()
                r = dialog.exec()
                if r == 100:
                    name = dialog.text.text()
                    temp = lib.Pointer([])
                    lib.data.load(lib.playlist_dir.joinpath(name), temp, default=[])
                    playlists.val[name] = temp
                    playlists_widget.insertTab(len(playlists.val.keys()), PlaylistWidget(temp), name)
                playlists_widget.setCurrentIndex(len(playlists.val.keys()))

        playlists_widget.currentChanged.connect(on_tab_change)

        playlists_widget.addTab(SongsWidget(), "Songs")
        for name, playlist in playlists.val.items():
            widget = PlaylistWidget(playlist)
            playlists_widget.addTab(widget, name)
        playlists_widget.addTab(new_playlist, "+")

        layout.addWidget(playlists_widget, 0, 0)
        layout.setColumnStretch(0, 2)

        self.timer = QTimer()
        self.timer.start(100)
        self.timer.timeout.connect(player.refresh)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)


class SongWidget(QWidget):
    def __init__(self, song_id: str):
        super().__init__()
        self.id = song_id
        layout = QHBoxLayout()
        if song_id not in song_data.val:
            raise IndexError("Song not found")
        songinfo = song_data.val[song_id]

        self.Button = QPushButton()
        buttonlayout = QHBoxLayout()
        self.Button.setLayout(buttonlayout)
        self.Button.setFixedHeight(80)

        self.Icon = QLabel()
        self.Icon.setPixmap(song_cover_info(song_id)[0])
        self.Icon.setFixedSize(60, 60)
        buttonlayout.addWidget(self.Icon)

        self.Info = QLabel(lib.string_replace(lib.config.val["songstring_qt"], songinfo))
        self.Info.setMinimumWidth(200)
        self.Info.setAlignment(Qt.AlignmentFlag.AlignCenter)
        buttonlayout.addWidget(self.Info)

        self.MenuButton = QPushButton()
        self.MenuButton.setIcon(QApplication.style().standardIcon(QStyle.StandardPixmap.SP_CommandLink))
        self.MenuButton.setFixedSize(30, 80)

        layout.addWidget(self.Button)
        layout.addWidget(self.MenuButton)
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)
        self.setMinimumWidth(300)


class thread(QThread):
    ended = pyqtSignal(object)

    def __init__(self, parent, func):
        super().__init__()
        if parent is not None:
            self.setParent(parent)
        self.func = func

    def run(self):
        self.func()
        self.ended.emit("")


class PlaylistWidget(QWidget):
    minimumwidth = 350

    def __init__(self, playlist: lib.Pointer) -> None:
        super().__init__()
        self.playlist = playlist
        layout = QGridLayout()
        shuffle = QPushButton("Shuffle")
        shuffle.clicked.connect(self.shuffle)
        layout.addWidget(shuffle)
        play = QPushButton("Play")
        play.clicked.connect(partial(self.playsong, 0))
        layout.addWidget(play, 0, 1)
        self.search = QLineEdit()
        self.search.textChanged.connect(self.search_suggest)
        self.search.returnPressed.connect(self.find_song)
        self.searchresults = QStandardItemModel()
        completion = QCompleter(self.searchresults, self)
        completion.setModelSorting(QCompleter.ModelSorting.CaseInsensitivelySortedModel)
        completion.setCompletionMode(QCompleter.CompletionMode.InlineCompletion)
        self.search.setCompleter(completion)
        layout.addWidget(self.search, 0, 2)
        self.searchtype = QComboBox()
        self.searchtype.addItem("songs")
        self.searchtype.addItem("videos")
        self.searchtype.setEditable(False)
        layout.addWidget(self.searchtype, 0, 3)
        self.playlistarea = QScrollArea()
        self.playlistarea.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.playlistbox = QWidget()
        self.playlistlayout = QVBoxLayout()
        self.playlisthash = 0
        # self.refresh()
        self.playlistbox.setLayout(self.playlistlayout)
        self.playlistarea.setWidget(self.playlistbox)
        self.playlistarea.setWidgetResizable(True)
        layout.addWidget(self.playlistarea, 1, 0, 2, 0)
        self.setLayout(layout)
        self.setMinimumWidth(self.minimumwidth)
        self.setMinimumHeight(400)

    def search_suggest(self, text: str):
        if len(text) > 2:
            self.searchresults.clear()
            if lib.yt.online:
                completions = lib.yt.get_search_suggestions(text)
                self.searchresults.appendRow([QStandardItem(val) for val in completions])

    def find_song(self):
        if lib.yt.online:
            def finish():
                self.playlist.val.append(song_info["videoId"])
                self.refresh()

            song_infos = lib.yt.search(self.search.text(), self.searchtype.currentText(), limit=1)[:lib.config.val["results"]]
            dialog = ChooseSongDialog(song_infos)
            r = dialog.exec()
            if r >= 100:
                song_info = song_infos[r - 100]
                th = thread(self, lambda: lib.download_song(song_info, wait=True))
                th.ended.connect(finish)
                th.start()

    def shuffle(self):
        if player.playlist == []:
            player.add_list(
                [lib.song_file(song) for song in self.playlist.val]
            )
        player.shuffle()

    def playsong(self, num: int):
        player.clear_list()
        player.add_list(
            [lib.song_file(song) for song in self.playlist.val[num:]]
        )

    def refresh(self):
        if self.playlisthash != lib.hash_container(self.playlist.val):
            self.playlisthash = lib.hash_container(self.playlist.val)
            clear_layout(self.playlistlayout)
            for i, val in enumerate(self.playlist.val):
                try:
                    self.playlistlayout.addWidget(self.nth_songwidget(i))
                except (IndexError):
                    pass

    def nth_songwidget(self, n: int):
        wid = SongWidget(self.playlist.val[n])
        wid.Button.clicked.connect(partial(self.playsong, n))
        menu = QMenu()
        append: QAction = menu.addAction("append")
        remove: QAction = menu.addAction("remove")
        insert: QAction = menu.addAction("play next")
        append.triggered.connect(partial(player.add, lib.song_file(self.playlist.val[n])))
        remove.triggered.connect(partial(self.remove_song, n))

        def insert_song(n):
            song: Path = lib.song_file(self.playlist.val[n])
            if player.playlist != []:
                player.playlist.insert(1, song)
            else:
                player.play(song)
        insert.triggered.connect(partial(insert_song, n))

        def contextmenu() -> None:
            menu.popup(QCursor.pos())

        wid.MenuButton.clicked.connect(contextmenu)
        return wid

    def remove_song(self, n):
        del self.playlist.val[n]
        self.refresh()


class ChooseSongDialog(QDialog):
    def __init__(self, songs: list):
        super().__init__()
        self.setWindowTitle("Choose Song")
        layout = QGridLayout()
        for i, song in enumerate(songs):
            wid = QPushButton(song["title"] + " - " + song["artists"][0]["name"])
            wid.clicked.connect(partial(self.done, i + 100))   # + 100 to tell apart from codes like 0 which is also emitted on window closing
            url = song["thumbnails"][0]["url"]
            image = QImage()
            image.loadFromData(requests.get(url).content)
            pixmap = QPixmap(image)
            wid.setIcon(QIcon(pixmap))
            wid.setFixedSize(500, 80)
            wid.setIconSize(QSize(60, 60))
            wid.setStyleSheet("font-size: 20px")
            layout.addWidget(wid, i, 0)
        self.setLayout(layout)
        self.setFixedSize(550, len(songs)*80+60)


class NewPlaylistDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Enter Name")
        layout = QVBoxLayout()
        self.text = QLineEdit()
        self.text.returnPressed.connect(partial(self.done, 100))
        layout.addWidget(self.text)
        self.setLayout(layout)
        self.setFixedSize(300, 60)


class SongsWidget(PlaylistWidget):
    def __init__(self) -> None:
        playlist = lib.Pointer(list(song_data.val.keys()))
        super().__init__(playlist)
        self.layout().removeWidget(self.search)
        self.layout().removeWidget(self.searchtype)
        self.search.setParent(None)
        self.searchtype.setParent(None)

    def remove_song(self, n):
        del song_data.val[self.playlist.val[n]]
        super().remove_song(n)

    def refresh(self):
        if self.playlisthash != hash(song_data):
            self.playlist = lib.Pointer(list(song_data.val.keys()))
            super().refresh()
            self.playlisthash = hash(song_data)


class PlayerWidget(QWidget, lib.MusicPlayer):
    def __init__(self):
        QWidget.__init__(self)
        lib.MusicPlayer.__init__(self)

        layout = QGridLayout()
        layout.setRowStretch(0, 3)
        self.Icon = QLabel()
        layout.addWidget(self.Icon, 0, 0, 1, 3, Qt.AlignmentFlag.AlignCenter)

        self.Button_f = QPushButton("")
        self.Button_f.setIcon(QApplication.style().standardIcon(QStyle.StandardPixmap.SP_MediaSkipForward))
        self.Button_f.clicked.connect(self.next)
        self.Button_f.setFixedWidth(80)
        self.Button_b = QPushButton("")
        self.Button_b.setIcon(QApplication.style().standardIcon(QStyle.StandardPixmap.SP_MediaSkipBackward))
        self.Button_b.clicked.connect(self.prev)
        self.Button_b.setFixedWidth(80)
        self.Button_play = QPushButton("")
        self.Button_play.setIcon(QApplication.style().standardIcon(QStyle.StandardPixmap.SP_MediaPlay))
        self.Button_play.clicked.connect(self.toggle)
        self.prog_bar = QProgressBar()

        self.title = QLabel()
        self.title.setFixedHeight(30)

        layout.addWidget(self.title, 1, 0, 1, 3, Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.prog_bar, 2, 0, 1, 3)
        layout.addWidget(self.Button_b, 3, 0)
        layout.addWidget(self.Button_play, 3, 1)
        layout.addWidget(self.Button_f, 3, 2)

        self.setAutoFillBackground(True)
        self.setLayout(layout)

    def toggle(self):
        super().toggle()
        if self.playing:
            self.Button_play.setIcon(QApplication.style().standardIcon(QStyle.StandardPixmap.SP_MediaPause))
        else:
            self.Button_play.setIcon(QApplication.style().standardIcon(QStyle.StandardPixmap.SP_MediaPlay))

    def get_icon_scale(self) -> int:
        size = self.parent().size()
        h, w = size.height(), size.width()
        return min(h - 150, w - PlaylistWidget.minimumwidth)

    def refresh(self):
        if self.playlist != []:
            self.query()
            song = self.song
            if player.song:
                player.Icon.setPixmap(song_cover_info(player.song, self.get_icon_scale())[0])
                try:
                    self.prog_bar.setRange(0, song_data.val[song]["duration_seconds"])
                    self.prog_bar.setValue(int(self.timer))
                    self.prog_bar.setFormat(f"{lib.format_time(int(self.timer))} - {song_data.val[song]['duration']}")
                    self.title.setText(song_data.val[song]['title'])
                except KeyError:
                    del self.playlist[self.counter]
                    self.counter = self.counter % len(self.playlist)
                    self.proc.kill()

    def play(self, file: Path):
        super().play(file)
        song = file.stem
        cover, color = song_cover_info(song, self.get_icon_scale())
        self.Icon.setPixmap(cover)
        self.parent().size()
        colors = self.palette()
        colors.setColor(QPalette.ColorRole.Window, color)
        self.setPalette(colors)


def song_cover_info(song_id: str, scale=60) -> tuple[QPixmap, QColor]:
    file = lib.song_file(song_id)
    metadata: eyed3.AudioFile = eyed3.load(file)
    image = QImage.fromData(metadata.tag.images[0].image_data)
    color = image.pixelColor(1, 1)
    width, height = image.width(), image.height()

    image = image.copy(int((width - height) / 2), 0, height, height)

    pixmap = QPixmap.fromImage(image)
    return pixmap.scaledToHeight(scale), color


def clear_layout(layout: QLayout):
    for i in reversed(range(layout.count())):
        layout.itemAt(i).widget().setParent(None)


def main(func=lambda: None):
    """initialises the GUI. func is a callable and executed right before the mainloop"""
    app = QApplication(sys.argv)
    theme = lib.config.val["theme"]
    logging.getLogger().info(f"theme:{theme}, available={QStyleFactory.keys()}")
    if theme in QStyleFactory.keys():
        app.setStyle(theme)
    window = MainWindow()
    func()
    window.show()
    try:
        app.exec()
    finally:
        player.proc.stop()
        lib.data.save_all()


if __name__ == "__main__":
    main()
