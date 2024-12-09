import logging
import os
from pathlib import Path

from spotdl import Spotdl
from spotdl.types.song import Song

from ..models import SpotDLTrackMetadata


class SpotDLClient:
    def __init__(self, client_id: str, client_secret: str, target_directory: Path = Path("music")):
        self.original_directory = os.getcwd()
        if not os.path.exists(target_directory):
            os.makedirs(target_directory)
        self.target_directory = target_directory
        self.spotdl = Spotdl(client_id=client_id, client_secret=client_secret)
        self.spotdl.downloader.settings["output"] = "{artists} - {title}.{output-ext}"
        self._logger = logging.getLogger(__name__)

    def search_and_download(self, query: list[str] | str) -> list[SpotDLTrackMetadata]:
        if isinstance(query, str):
            query = [query]
        self._logger.info("Searching for songs with query [ '%s' ]", query)
        songs = self.spotdl.search(query)
        songs_metadata = self._get_track_metadata(songs)
        songs_to_download = [
            song_metadata.song for song_metadata in songs_metadata if not os.path.exists(song_metadata.download_path)
        ]
        self._logger.info(
            "Downloading [ %d/%d ] songs to [ '%s' ]",
            len(songs_to_download),
            len(songs),
            self.target_directory,
        )
        os.chdir(self.target_directory)
        self.spotdl.download_songs(songs_to_download)
        os.chdir(self.original_directory)
        return songs_metadata

    def _get_track_metadata(self, songs: list[Song]) -> list[SpotDLTrackMetadata]:
        metadata = []
        for song in songs:
            metadata.append(
                SpotDLTrackMetadata(
                    artists=song.artists,
                    download_root=self.target_directory,
                    name=song.name,
                    duration_ms=song.duration * 1000,  # convert to ms
                    album_name=song.album_name,
                    image_url=song.cover_url,
                    release_year=song.year,
                    disc_number=song.disc_number,
                    track_number=song.track_number,
                    id=song.song_id,
                    is_playable=True,  # always True for Spotify songs, not provided by SpotDL
                    song=song,
                )
            )
        return metadata
