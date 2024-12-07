import os

from pydantic import BaseModel

from ..utils import fix_filename


class TrackMetadata(BaseModel):
    artists: list[str]
    download_root: str
    name: str
    duration_ms: int
    album_name: str | None = None
    image_url: str | None = None
    release_year: str | None = None
    disc_number: int | None = None
    track_number: int | None = None
    id: str | None = None
    is_playable: bool | None = None

    @property
    def artist_and_name(self) -> str:
        return f"{self.artists[0]} - {self.name}"

    @property
    def duration_seconds(self) -> int:
        if self.duration_ms is None:
            return 0
        return self.duration_ms // 1000

    @property
    def filename(self) -> str:
        filename = fix_filename(f"{self.artist_and_name}.mp3")
        return filename

    @property
    def download_path(self) -> str:
        return os.path.join(self.download_root, self.filename)


class SpotifyTrackMetadata(TrackMetadata):
    pass
