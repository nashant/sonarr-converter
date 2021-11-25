import ffmpeg

from dataclasses import dataclass
from typing import List
from os import rename, remove
from os.path import basename, dirname, isfile


@dataclass
class EpisodeFile():
    path: str
    tmppath: str
    codecs: List[str]

    @classmethod
    def from_sonarr_post(cls, episodeFile: dict, **kwargs):
        path = episodeFile['path']
        if not isfile(path):
            raise FileNotFoundError

        tmppath = f"{dirname(path)}/.{basename(path)}"
        p = ffmpeg.probe(path)
        codecs = map(lambda s: s["codec_name"], p["streams"])
        return cls(path=path, tmppath=tmppath, codecs=codecs)
    
    @property
    def has_asses(self):
        return 'ass' in self.codecs

    def convert_ass_to_srt(self):
        stdout, stderr = (
            ffmpeg.input(self.path)
            .output(self.tmppath, vcodec='copy', acodec='copy', scodec='srt')
            .run(capture_stdout=True, capture_stderr=True)
        )
        remove(self.path)
        rename(self.tmppath, self.path)

