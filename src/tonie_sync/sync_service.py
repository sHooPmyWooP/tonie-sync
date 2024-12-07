import logging
import os
from pathlib import Path
from typing import Annotated

from pydantic import AfterValidator, AnyUrl, BaseModel, EmailStr, field_validator
from pydantic_settings import BaseSettings

from .clients import SpotifyClient, TonieClient

HttpUrlString = Annotated[AnyUrl, AfterValidator(str)]


class SyncServiceConfig(BaseSettings):
    spotify_username: str
    spotify_password: str
    tonie_username: EmailStr
    tonie_password: str
    tonie_household: str
    creative_tonie_name: str
    sync_url: HttpUrlString
    data_path: Path

    @field_validator("data_path", mode="before")
    def validate_data_path(cls, v):
        return Path(v)


class SyncService(BaseModel):
    config: SyncServiceConfig = SyncServiceConfig()

    def sync(self):
        spotify_client = SpotifyClient(
            username=self.config.spotify_username,
            password=self.config.spotify_password,
            data_path=self.config.data_path,
        )
        tonie_client = TonieClient(
            email=self.config.tonie_username,
            password=self.config.tonie_password,
            household=self.config.tonie_household,
        )

        download_root = os.path.join(self.config.data_path, "downloads")
        if not os.path.exists(download_root):
            logging.info(f"Creating download folder {download_root}")
            os.makedirs(download_root)

        download_tracks_metadata = spotify_client.download_tracks(
            download_root,
            self.config.sync_url,
        )

        for track_metadata in download_tracks_metadata:
            self.spotify_client.process_track(track_metadata)

        tonie_client.update_creative_tonie(self.config.creative_tonie_name, download_tracks_metadata)
