from enum import Enum
from dataclasses import dataclass
import typing
from collections import namedtuple


class RepeatState(Enum):
    QUEUE = 0
    TRACK = 1
    OFF = 2


@dataclass
class Track:
    album_id: int = 0
    artist_id: int = 0
    track_id: int = 0
    title: str = ""
    artist: str = ""
    album: str = ""
    pos: int = 0
    service: str = ""

    def __init__(self, xml_tag):
        for k, v in xml_tag.attrib.items():
            if k == "albumid":
                self.album_id = int(v)
            elif k == "service":
                self.service = v
            elif k == "artistid":
                self.artist_id = int(v)
            elif k == "songid":
                self.track_id = int(v)
            elif k == "id":
                self.pos = int(v)
        for song_props in xml_tag:
            if song_props.tag == "title":
                self.title = song_props.text
            elif song_props.tag == "art":
                self.artist = song_props.text
            elif song_props.tag == "alb":
                self.album = song_props.text


@dataclass
class Playlist:
    name: str
    modified: bool
    length: int
    playlist_id: int
    tracks: typing.List[Track]
