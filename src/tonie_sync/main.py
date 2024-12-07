import logging

import sys

from tonie_sync.sync_service import SyncService

logging.basicConfig(
    stream=sys.stdout,
    level=logging.INFO,
    format="%(asctime)s | %(message)s",
)


def main():
    """Sync the files to the creative tonie based on the configuration."""
    sync_service = SyncService()
    sync_service.sync()


if __name__ == "__main__":
    main()
