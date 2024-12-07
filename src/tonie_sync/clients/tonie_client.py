import logging

from tonie_api.api import TonieAPI
from tonie_api.models import CreativeTonie

from ..models.track_metadata import TrackMetadata
from ..utils import format_seconds


class TonieClient:
    """A client for interacting with the Tonie API."""

    def __init__(self, email: str, password: str, household: str):
        self.api = TonieAPI(email, password)
        self.household = self._get_household(household)

    def _get_household(self, household_name: str):
        """Get the household object by its name.

        Args:
            household_name: The name of the household to retrieve.

        Returns:
            Household: The household object that matches the given name.

        Raises:
            ValueError: If no household with the specified name is found.
        """
        household = next((x for x in self.api.get_households() if x.name == household_name), None)
        if household is None:
            raise ValueError(f"Household [ '{household_name}' ] not found!")
        return household

    def update_creative_tonie(self, creative_tonie_name: str, tracks_metadata: list[TrackMetadata]):
        creative_tonie = self.get_creative_tonie_by_name(creative_tonie_name)
        track_file_names = [track.artist_and_name for track in tracks_metadata]
        self.remove_orphaned_chapters(creative_tonie, track_file_names)
        self.upload_tracks_to_creative_tonie(creative_tonie_name, tracks_metadata)
        self.sort_chapters(creative_tonie_name, tracks_metadata)

    def get_creative_tonie_by_name(self, creative_tonie_name: str) -> CreativeTonie:
        """Retrieve a CreativeTonie object by its name from a specified household.

        Args:
            creative_tonie_name: The name of the CreativeTonie to retrieve.

        Returns:
            CreativeTonie: The CreativeTonie object that matches the given name.

        Raises:
            ValueError: If no CreativeTonie with the specified name is found in the household.
        """
        creative_tonie = next(
            (x for x in self.api.get_all_creative_tonies_by_household(self.household) if x.name == creative_tonie_name),
            None,
        )
        if creative_tonie is None:
            raise ValueError(f"Creative Tonie '{creative_tonie_name}' not found!")
        return creative_tonie

    def remove_orphaned_chapters(self, creative_tonie, track_file_names: list[str]):
        logging.info("Removing orphaned chapters from creative tonie...")
        chapters = creative_tonie.chapters
        chapters_to_keep = [chapter for chapter in chapters if chapter.title in track_file_names]
        if chapters_to_keep:
            logging.info(
                f"Keeping chapters: {', '.join(
                [chapter.title for chapter in chapters_to_keep])}"
            )
            self.api.sort_chapter_of_tonie(creative_tonie, chapters_to_keep)
        else:
            logging.info("No chapters to keep found! Deleting all chapters...")
            self.api.clear_all_chapter_of_tonie(creative_tonie)
        return chapters

    def sort_chapters(self, creative_tonie_name, tracks_metadata):
        logging.info("Sorting chapters...")
        chapters_sorted = False
        creative_tonie = self.get_creative_tonie_by_name(creative_tonie_name)
        for num, track_metadata in enumerate(tracks_metadata):
            oldchapterIndex = next(
                (i for i, item in enumerate(creative_tonie.chapters) if item.title == track_metadata.name),
                -1,
            )
            if oldchapterIndex != -1 and num != oldchapterIndex:
                creative_tonie.chapters.insert(num, creative_tonie.chapters.pop(oldchapterIndex))
                chapters_sorted = True
        if chapters_sorted:
            logging.info("Sorting changed...")
            self.api.sort_chapter_of_tonie(creative_tonie, creative_tonie.chapters)
        else:
            logging.info("No sorting needed...")

    def upload_tracks_to_creative_tonie(self, creative_tonie_name, tracks_metadata: list[TrackMetadata]):
        logging.info("Uploading new tracks / chapters...")
        for track_metadata in tracks_metadata:
            self.upload_track(creative_tonie_name, track_metadata)

    def upload_track(
        self,
        creative_tonie_name: str,
        track_metadata: TrackMetadata,
    ):
        creative_tonie = self.get_creative_tonie_by_name(creative_tonie_name)  # TODO: cache this
        chapters = creative_tonie.chapters
        tonie_seconds_remaining = creative_tonie.secondsRemaining
        found_on_creative_tonie = next((x for x in chapters if x.title == track_metadata.artist_and_name), None)

        if found_on_creative_tonie is not None:
            logging.info(f"... skipping '{track_metadata.artist_and_name}' => already present on creative tonie")
            return

        if tonie_seconds_remaining - track_metadata.duration_seconds <= 0:
            logging.warning(
                f"... skipping {track_metadata.artist_and_name} => Not enough free space! Needed: {format_seconds(track_metadata.duration_seconds)} | Free: {format_seconds(tonie_seconds_remaining)}"
            )
            return

        logging.info(f"... uploading '{track_metadata.artist_and_name}' to creative tonie")
        self.api.upload_file_to_tonie(
            creative_tonie,
            track_metadata.download_path,
            track_metadata.artist_and_name,
        )
        tonie_seconds_remaining = tonie_seconds_remaining - track_metadata.duration_seconds
        logging.info(f"... upload complete! => {format_seconds(tonie_seconds_remaining)} free")
