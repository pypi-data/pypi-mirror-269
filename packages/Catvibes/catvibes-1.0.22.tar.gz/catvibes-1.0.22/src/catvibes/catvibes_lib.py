import _curses
import curses
import sys
import json
import os
import random
import re
import shutil
import time
import logging
from pathlib import Path
import threading as th
from typing import Callable, Iterable

import yt_dlp
import ytmusicapi
import vlc

# placeholders for directories
main_dir: Path
song_dir: Path
data_dir: Path
playlist_dir: Path


def hash_container(container: Iterable) -> int:
    """hashes a typically unhashable Object (like list or dict by adding all hashes of items)"""
    hashval = 0
    for i in container:
        try:
            hashval += hash(i) / 1000
        except TypeError:
            hashval += hash_container(i)
    return int(hashval)


class Pointer:
    """a VERY bad implementation of pointers. use .val to retrieve or set value"""

    def __init__(self, val):
        self.val = val

    def __hash__(self) -> int:
        try:
            return hash(self.val)
        except:
            return hash_container(self.val)


playlists = Pointer({})
song_data = Pointer({})
config = Pointer({})


def init():
    """loads files and config"""
    # global was never intended to be used this way... oh pythongod forgive my sins
    global playlists, song_data, data, main_dir, config, song_dir, data_dir, playlist_dir, music_player, config_location, yt
    workdir = Path(__file__).parent

    default_config_location = workdir.joinpath("config")
    config_base = os.environ.get('APPDATA') or \
        os.environ.get('XDG_CONFIG_HOME') or \
        os.path.join(os.environ['HOME'], '.config')
    config_location = Path(config_base).joinpath("Catvibes/config")
    if not Path.is_file(config_location):
        os.makedirs(config_location.parent, exist_ok=True)
        shutil.copy2(default_config_location, config_location.parent)

    data = Datamanager()

    data.load(config_location, config)

    main_dir = Path.home().joinpath(config.val["maindirectory"])
    song_dir = main_dir.joinpath("songs")
    os.makedirs(song_dir, exist_ok=True)
    data_dir = main_dir.joinpath("data")
    os.makedirs(data_dir, exist_ok=True)
    playlist_dir = main_dir.joinpath("playlists")
    os.makedirs(playlist_dir, exist_ok=True)
    logfile = main_dir.joinpath("catvibes.log")
    if Path.is_file(logfile):
        shutil.copy2(logfile, main_dir.joinpath("prev_log.log"))

    data.create_if_not_exsisting(logfile, "")
    logging.basicConfig(filename=str(logfile), filemode="w", encoding="utf-8", format="%(asctime)s: %(message)s", datefmt="%m/%d/%y %H:%M:%S", level=logging.INFO)
    # loads the song db
    data.load(data_dir.joinpath("data"), song_data, {})

    # fix for pyinstaller & python-vlc
    if sys.platform.startswith("linux"):
        os.environ["VLC_PLUGIN_PATH"] = "/usr/lib64/vlc/plugins"
    if sys.platform.startswith("win"):
        ffmpeg_path = Path(__file__).parent
        os.environ["PATH"] += os.pathsep + os.path.dirname(ffmpeg_path)
        os.environ["VLC_PLUGIN_PATH"] = "C:\\Program Files\\VideoLAN\\VLC\\plugins"

    os.makedirs(playlist_dir, exist_ok=True)
    with os.scandir(playlist_dir) as files:
        for f in files:
            name = Path(f).stem
            logging.info(f"loaded playlist {name}")
            temp = Pointer([])
            data.load(Path(f), temp)
            playlists.val[name] = temp
    music_player = MusicPlayer()
    yt = YTInterface()


class YTInterface:
    def __init__(self):
        self.yt = ytmusicapi.YTMusic()
        self.connect()

    def search(self, *args, **kwargs) -> list[dict]:
        if self.online:
            return self.yt.search(*args, **kwargs)
        else:
            raise self.offline_error

    def get_search_suggestions(self, *args, **kwargs) -> list[str]:
        if self.online:
            return self.yt.get_search_suggestions(*args, **kwargs)
        else:
            raise self.offline_error

    def get_song(self, song_id: str) -> dict:
        if self.online:
            return self.yt.get_song(song_id)
        else:
            raise self.offline_error

    def connect(self):
        self.online = True
        try:
            self.yt.search("test")
        except:
            self.online = False

    @property
    def offline_error(self) -> Exception:
        self.connect()
        return Exception("you are offline")


class DisplayTab:
    """# base_class for other tabs"""

    def __init__(self, window, title: str, linestart: int = 0):
        self.screen = window
        self.title = title
        self.keyhandler: dict[str, Callable] = {}
        self.line = linestart
        self.maxy, self.maxx = self.screen.getmaxyx()
        self.on_key("KEY_UP", self.up)
        self.on_key("KEY_DOWN", self.down)

    def on_key(self, key: str, f):
        """registers functions with key strings like KEY_LEFT"""
        self.keyhandler[key] = f

    @property
    def maxlines(self) -> int:
        return 0

    def up(self):
        """goes one line up"""
        if self.maxlines > 0:
            self.line = (self.line - 1) % self.maxlines

    def down(self):
        """goes one line down"""
        if self.maxlines > 0:
            self.line = (self.line + 1) % self.maxlines

    def handle_key(self, key: str):
        """tries to do actions a defined with on_key()"""
        if key in self.keyhandler:
            self.keyhandler[key]()

    def disp(self):
        pass


class PlaylistTab(DisplayTab):
    """a tab for simply interacting with playlists"""

    def __init__(self, window, title: str, playlist: Pointer, linestart: int = 0):
        super().__init__(window, title, linestart=linestart)
        self.playlist = playlist
        self.on_key("f", self.add_song)
        self.on_key("p", self.play_playlist)
        self.on_key("a", self.add_song_to_queue)
        self.on_key("d", self.remove_song)
        self.on_key(" ", self.play_or_pause)
        self.on_key("r", self.shuffle)
        self.on_key("n", self.next)
        self.on_key("b", self.prev)

    @property
    def maxlines(self):
        return len(self.playlist.val)

    def disp(self):
        """displays the playlist on the screen"""
        start = 0
        end = 0
        playlist_view = []
        self.maxy, self.maxx = self.screen.getmaxyx()
        self.screen.clear()
        if self.maxy > len(self.playlist.val):  # is the window big enough for all songs
            start = 0
            end = len(self.playlist.val)
            playlist_view = self.playlist.val
        else:  # if not, then
            half = int(self.maxy / 2)
            odd_max = 0 if half == self.maxy / 2 else 1
            if self.line < half:
                start = 0
                end = self.maxy
            elif self.line > len(self.playlist.val) - half - 1:
                end = len(self.playlist.val)
                start = end - self.maxy
            else:
                start = self.line - half
                end = self.line + half + odd_max

            playlist_view = self.playlist.val[start:end]

        for i, song in enumerate(playlist_view):
            try:
                if i == self.line - start:
                    addstr(self.screen, i, 0, song_string(song_data.val[song]), curses.A_REVERSE)
                else:
                    addstr(self.screen, i, 0, song_string(song_data.val[song]))
            except KeyError:
                info(self.screen, f"a song with id {song} was not found. ")
                self.playlist.val.remove(song)
            except _curses.error:
                pass  # bad practise but required for smaller windows
        self.screen.refresh()

    def add_song(self):
        """ searches for a song and adds it to the playlist"""
        result = search(self.screen)
        if result is not None:
            def finished():
                self.playlist.val.append(result["videoId"])
                self.line = len(self.playlist.val) - 1
                self.disp()
            download_song(result, wait=True, on_finished=finished)

    def remove_song(self):
        """removes the selected song from the playlist"""
        del self.playlist.val[self.line]
        if self.maxlines > 0:
            self.line = self.line % self.maxlines

    def play_playlist(self):
        """plays this playlist from the start"""
        music_player.clear_list()
        music_player.add_list(
            [song_file(self.playlist.val[i]) for i in range(self.line, self.maxlines)]
        )

    def add_song_to_queue(self):
        """appends the selected song to the queue"""
        music_player.add(song_file(self.playlist.val[self.line]))

    def shuffle(self):
        """plays the whole playlist in shuffeled order"""
        self.play_playlist()
        music_player.shuffle()

    @staticmethod
    def play_or_pause():
        """ plays / pauses depending on current state"""
        music_player.toggle()

    @staticmethod
    def next():
        """skip to the next song"""
        music_player.next()

    @staticmethod
    def prev():
        """skips to the previous song"""
        music_player.prev()

    def new_playlist(self):
        """creates a new playlist. currently requires restart to list playlist"""
        name = inputstr(self.screen, "Name of the playlist: ")
        if name is not None:
            temp = Pointer([])
            data.load(playlist_dir.joinpath(name), temp, default=[])
            playlists.val[name] = temp.val


class SongsTab(PlaylistTab):
    """a tab for all songs"""

    def __init__(self, screen):
        super().__init__(screen, "Songs", Pointer([]))
        self.playlist.val = list(song_data.val.keys())
        self.on_key("d", self.del_song_from_db)
        del self.keyhandler["f"]

    def del_song_from_db(self):
        """deletes a song from everything"""
        song_id = self.playlist.val[self.line]
        try:
            del song_data.val[song_id]
            del self.playlist.val[self.line]
        except IndexError:
            info(self.screen, f"Cannot delete that Song {song_id}. ")
            return
        for playlist in playlists.val.items():
            while song_id in playlist:
                playlist.remove(song_id)

    def disp(self):
        self.playlist.val = list(song_data.val.keys())
        super().disp()


class Datamanager:
    """a class for saving and loading variables to files"""

    def __init__(self):
        # files[i] and vars[i] belong together
        self.files: list[Path] = []
        self.vars: list[Pointer] = []

    def load(self, file: Path, to: Pointer, default=None):
        """loads and links a file to a variable. if the file is nonexistent load default and create file"""
        if default is None:
            default = {}
        self.create_if_not_exsisting(file, default)
        with open(file, "r") as loaded_file:
            to.val = json.load(loaded_file)
        self.vars.append(to)
        self.files.append(file)

    @staticmethod
    def save(var: Pointer, file=Path):
        """saves a variable to a file"""
        if var.val is not None:
            with open(file, "w") as f:
                f.write(json.dumps(var.val, indent=4))

    def save_all(self):
        """saves all var:file associations"""
        for i in range(len(self.files)):
            var_pointer = self.vars[i]
            file = self.files[i]
            self.save(var_pointer, file)
        logging.info("saved all files")

    @staticmethod
    def create_if_not_exsisting(file, content):
        """if the given file doesn't exist, create it with content"""
        if not Path.is_file(file):
            filepath = file.parent
            os.makedirs(filepath, exist_ok=True)
            with open(file, "x") as f:
                f.write(json.dumps(content))


class MusicPlayer:
    """a class for playing files"""

    def __init__(self) -> None:
        self.playlist: list = []
        self.counter: int = -1
        self.proc: MediaPlayer = vlc.MediaPlayer()
        self.playing: bool = False

    @property
    def timer(self):
        return int(self.proc.get_time() / 1000)

    def play(self, file: Path):
        self.proc.set_media(vlc.Media(file))
        self.proc.play()
        self.playing = True

    def pause(self):
        self.playing = False
        self.proc.pause()

    def continu(self):
        if self.playlist != []:
            self.playing = True
            self.proc.play()

    def toggle(self):
        if self.playing:
            self.pause()
        else:
            self.continu()

    def add(self, file: Path):
        self.playlist.append(file)
        if self.counter == -1:
            self.counter = 0
            self.play(self.playlist[0])

    def add_list(self, songs: list[Path]):
        for file in songs:
            self.add(file)

    def clear_list(self):
        self.playlist = []
        self.counter = -1

    def query(self):
        if self.proc.get_state() == 6:
            if self.counter < len(self.playlist) - 1:
                self.counter += 1
                self.play(self.playlist[self.counter])
            else:
                self.playing = False

    def shuffle(self):
        random.shuffle(self.playlist)
        self.counter = 0
        self.play(self.playlist[self.counter])

    def next(self):
        if len(self.playlist) > 0:
            self.counter = (self.counter + 1) % len(self.playlist)
            self.play(self.playlist[self.counter])

    def prev(self):
        if len(self.playlist) > 0:
            self.counter = (self.counter - 1) % len(self.playlist)
            self.play(self.playlist[self.counter])

    @property
    def song(self):
        if self.playlist != []:
            return self.playlist[self.counter].stem
        return None


class MusicPlayerWithScreen(MusicPlayer):
    def __init__(self, screen):
        super().__init__()
        self.screen = screen

    def disp(self):
        self.screen.clear()
        if self.playing:
            file = self.playlist[self.counter]
            song_id = file.stem
            addstr(self.screen, 0, 0, info_string(song_data.val[song_id], self.timer))
            self.screen.refresh()

    def query(self):
        super().query()
        self.disp()

    def play(self, file: Path):
        super().play(file)
        self.disp()


music_player: MusicPlayer  # placeholder for musicplayer
data: Datamanager  # placeholder for Datamanager


def delline(screen, y: int, refresh=False):
    screen.move(y, 0)
    screen.clrtoeol()
    if refresh:
        screen.refresh()


def inputchoice(screen, choices: list) -> int:
    """displays a number of choices to the user and returns the chosen number. -1 if exited"""
    maxy, _ = getmax(screen)
    for i, choice in enumerate(choices):
        delline(screen, maxy - len(choices) + i + 1)
        addstr(screen, maxy - len(choices) + i + 1, 0, f"{i + 1}. {choice}")
    screen.refresh()
    key = -1
    while key < 1 or key > len(choices):
        key = screen.getkey()
        try:
            key = int(key)
        except ValueError:
            if key == "\x1b":
                key = 0
                break
            key = -1
    for i in range(maxy - len(choices), maxy):
        delline(screen, i + 1)
    screen.refresh()
    return key - 1


def search(screen):
    """asks and searches for a song on YouTube and returns a corresponding song_info dict"""
    search_str = inputstr(screen, "Search Song: ")
    if search_str is None:
        return
    try:
        results = yt.search(search_str, filter="songs", limit=config.val["results"])
    except Exception as e:
        e = str(e).replace('\n', '')
        info(screen, f"Something went wrong searching Youtube: {e}")
        return
    num_results = config.val["results"]
    choices = [song_string(results[i]) for i in range(num_results)]
    chosen = inputchoice(screen, choices)
    if chosen == -1:
        return
    chosen = results[chosen]
    return chosen


def inputstr(screen, question: str) -> str | None:
    """asks for a simple textinput"""
    maxy, _ = getmax(screen)
    delline(screen, maxy)
    addstr(screen, maxy, 0, question)
    screen.refresh()
    text = ""
    key = screen.getkey()
    while key != "\n":
        if key == "\x7f":  # enter
            text = text[:-1]
        elif key == "\x1b":  # escape
            return
        else:
            text += key
        addstr(screen, maxy, len(question), text + "   ")
        screen.refresh()
        key = screen.getkey()
    delline(screen, maxy, True)
    return text


def info(screen, text: str, important=True) -> None:
    """prints a message at the bottom of the screen"""
    maxy, _ = getmax(screen)
    addstr(screen, maxy, 0, text + " press any key to continue")
    screen.refresh()
    if important:
        screen.getkey()
        delline(screen, maxy, True)


def download_song(song_info: dict, wait=False, on_finished=lambda: None) -> None:
    """downloads a song from a song_info dict returned by yt.search()"""
    song_id = song_info["videoId"]

    def save_data():
        song_data.val[song_id] = song_info
        data.save_all()
        on_finished()

    if Path.is_file(song_dir.joinpath(f"{song_id}.mp3")):
        save_data()
        return

    def run_download(song_id: str):

        # generated by cli_to_api.py https://github.com/yt-dlp/yt-dlp/blob/master/devscripts/cli_to_api.py
        yt_dlp_opts = {'extract_flat': 'discard_in_playlist',
                       'final_ext': 'mp3',
                       'format': 'bestaudio/best',
                       'fragment_retries': 10,
                       'ignoreerrors': 'only_download',
                       'outtmpl': {'default': f"{song_dir}/{song_id}.mp3", 'pl_thumbnail': ''},
                       'postprocessors': [{'key': 'FFmpegExtractAudio',
                                           'nopostoverwrites': False,
                                           'preferredcodec': 'mp3',
                                           'preferredquality': '0'},
                                          {'add_chapters': True,
                                           'add_infojson': 'if_exists',
                                           'add_metadata': True,
                                           'key': 'FFmpegMetadata'},
                                          {'already_have_thumbnail': False, 'key': 'EmbedThumbnail'},
                                          {'key': 'FFmpegConcat',
                                           'only_multi_video': True,
                                           'when': 'playlist'}],
                       'retries': 10,
                       'writethumbnail': True}

        with yt_dlp.YoutubeDL(yt_dlp_opts) as ydl:
            ydl.download([f"https://www.youtube.com/watch?v={song_id}"])

        save_data()
        logging.info("finished")

    download_thread = th.Thread(target=run_download, args=[song_id])
    logging.info(f"started download of song: {song_info['title']}")
    download_thread.start()
    if wait:
        download_thread.join()


def song_file(song_id: str) -> Path:
    """returns the Path to a song by id"""
    return Path(f"{song_dir}/{song_id}.mp3")


def song_string(song_info: dict) -> str:
    """returns a string representation for a song_info dict according to config"""
    string = config.val["songstring"]
    return string_replace(string, song_info)


def info_string(song_info: dict, play_time: float) -> str:
    """returns a string representing the currently playing track"""
    string = config.val["infostring"]

    formatted_time = format_time(int(play_time))
    string = string.replace("CURRENT_TIME", formatted_time)

    progress = int(int(play_time) / song_info["duration_seconds"] * config.val["barlenght"])
    bar = "═" * progress + "‣" + "─" * (config.val["barlenght"] - progress - 1)
    string = string.replace("BAR", bar)

    return string_replace(string, song_info)


def format_time(seconds: int) -> str:
    formatted_time = time.strftime("%H:%M:%S", time.gmtime(seconds))
    prefix = str(re.findall("^[0:]{1,4}", formatted_time)[0])
    formatted_time = formatted_time.replace(prefix, "")
    return formatted_time


def string_replace(string: str, song_info) -> str:
    """replaces varoius KEYs in a string like TITLE with the info in the song_info dict"""
    try:
        string = string.replace("TITLE", song_info["title"])
    except:
        string = string.replace("TITLE", "")

    try:
        string = string.replace("ARTIST", song_info["artists"][0]["name"])
    except:
        string = string.replace("ARTIST", "")

    try:
        string = string.replace("LENGHT", song_info["duration"])
    except:
        string = string.replace("LENGHT", "")
    return string


def getmax(screen) -> tuple[int, int]:
    """returns the bottom most corner of the screen"""
    maxy, maxx = screen.getmaxyx()
    return maxy - 1, maxx - 1


def addstr(screen, y: int, x: int, string: str, params=None) -> None:
    try:
        if params is not None:
            screen.addstr(y, x, string, params)
        else:
            screen.addstr(y, x, string)
    except _curses.error:
        pass  # bad practise but required for smaller windows
