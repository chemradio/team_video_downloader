import threading
from pathlib import Path
from file_operator import init_folders, init_txt_files
from download_video import video_downloader_worker
from request_parser import video_request_loop


with open("basedir.txt", "r") as f:
    BASE_DIR = Path(f.read().strip())
USERS = [f.name for f in BASE_DIR.iterdir() if f.is_dir()]
TEMP_DIR = Path.cwd() / "temp"
VIDEO_DOWNLOADER_THREADS = 1


if __name__ == "__main__":
    init_folders(TEMP_DIR, BASE_DIR, USERS)
    init_txt_files(BASE_DIR, USERS, erase_existing=False)

    global_queue = []
    queue_lock = threading.RLock()

    request_thread = threading.Thread(
        target=video_request_loop,
        args=(global_queue, queue_lock, USERS, BASE_DIR, TEMP_DIR),
    )
    downloader_threads = [
        threading.Thread(
            target=video_downloader_worker,
            args=(global_queue, queue_lock, True),
        )
        for _ in range(VIDEO_DOWNLOADER_THREADS)
    ]

    request_thread.start()
    for downloader_thread in downloader_threads:
        downloader_thread.start()

    request_thread.join()
    for downloader_thread in downloader_threads:
        downloader_thread.join()
