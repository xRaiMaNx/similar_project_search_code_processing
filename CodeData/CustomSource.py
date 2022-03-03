from preprocess.sources import BaseSource
from pathlib import Path
from typing import Iterable

class CustomSource(BaseSource):
    """Source for working with a repository folder."""

    def __init__(self, path: str, **kwargs):
        """Initialize FolderSource class.

        Args:
            path: path to read folders from
            **kwargs: additional keyword arguments for FolderSource
        """
        self.path: str = path
        super(CustomSource, self).__init__(**kwargs)

    def directories(self) -> Iterable[Path]:
        yield Path(self.path)
