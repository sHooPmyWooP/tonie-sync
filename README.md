# Tonie Sync

A package to sync Spotify playlists to creative tonies.

> This package is not affiliated with Spotify or Tonies. It uses the Spotify and
> Tonie APIs to sync playlists to creative tonies. The package is intended for
> personal use only. Use at your own risk.
>
> The package is heavily inspired by
> [spoonie](https://github.com/Seji64/spoonie).

## Installation

```bash
pip install tonie-sync
```

This package requires these additional dependencies:

- ffmpeg

## Usage

```python
from tonie_sync import SyncService

sync_service = SyncService()  # Create a new SyncService instance with settings from environment variables
sync_service.sync()  # Sync the Spotify playlists to the creative tonies
```

## Environment Variables

| Environment Variable | Description                      | Example Value                                         |
| -------------------- | -------------------------------- | ----------------------------------------------------- |
| SPOTIFY_USERNAME     | Spotify account username         | 123456789                                             |
| SPOTIFY_PASSWORD     | Spotify account password         | this_is_very_secret                                   |
| TONIE_USERNAME       | Tonie account email              | my_email@provider.com                                 |
| TONIE_PASSWORD       | Tonie account password           | another_secret                                        |
| TONIE_HOUSEHOLD      | Name of the Tonie household      | My Household                                          |
| CREATIVE_TONIE_NAME  | Name of the creative Tonie       | Creative-Tonie                                        |
| SYNC_URL             | URL to the Spotify playlist      | https://open.spotify.com/playlist/poasdfa0s08sa76d5f9 |
| DATA_PATH            | Path to the local data directory | ./.local                                              |
