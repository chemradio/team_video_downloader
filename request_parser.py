import time
import threading
from pathlib import Path
from request_class import VideoDownloadRequest
from file_operator import check_filesize_changed, read_and_erase_request_file


def video_request_loop(
    queue: list[VideoDownloadRequest],
    queue_lock: threading.RLock,
    users: list[str],
    base_dir: Path,
    temp_dir: Path,
    refresh_interval: int = 10,
):
    request_file_sizes = {user: -1 for user in users}
    while True:
        for user in users:
            request_file = base_dir / f"{user}.txt"
            if request_file.exists():
                if check_filesize_changed(request_file, request_file_sizes[user]):
                    print(f"Processing video request for {user}...")
                    requested_urls = read_and_erase_request_file(request_file)
                    with queue_lock:
                        queue.extend(
                            [
                                VideoDownloadRequest(
                                    url=url,
                                    user=user,
                                    output_path=base_dir / user,
                                    timestamp=int(time.time()),
                                    temp_path=temp_dir,
                                )
                                for url in requested_urls
                            ]
                        )
        time.sleep(refresh_interval)
