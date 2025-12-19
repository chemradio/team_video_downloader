from dataclasses import dataclass
from pathlib import Path


@dataclass
class VideoDownloadRequest:
    url: str
    user: str
    output_path: Path
    temp_path: Path | None = None
    timestamp: int | None = None
