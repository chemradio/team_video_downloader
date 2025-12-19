import time
import yt_dlp
import threading
from pathlib import Path
from request_class import VideoDownloadRequest

YDL_OPTS = {
    "cookies": "cookies_netscape.txt",
    "extractor_args": {
        "youtube": {
            "player_client": ["default", "-tv_simply"],
        },
    },
    "verbose": True,
    "format": "bestvideo+bestaudio/best",
    "outtmpl": "%(uploader)s $ %(title).30s %(upload_date>%Y-%m-%d)s.%(ext)s",
}

CONVERT_OPTS = {
    "merge_output_format": "mp4",
    "remux_video": "mp4",
    "postprocessors": [
        {
            "key": "FFmpegVideoConvertor",
            "preferedformat": "mp4",
        }
    ],
    "postprocessor_args": [
        #############################
        # # nvenc
        # "-c:v",
        # "h264_nvenc",
        # "-preset",
        # "p4",  # Turing NVENC preset
        # "-cq",
        # "23",  # constant quality mode (good balance)
        # "-b:v",
        # "0",  # needed with CQ mode
        # "-c:a",
        # "aac",
        # "-b:a",
        # "192k",
        # #########################
        # nvenс fast
        "-c:v",
        "h264_nvenc",
        "-preset",
        "p1",  # FASTEST
        "-rc:v",
        "vbr",
        "-b:v",
        "5000k",  # adjust as needed
        "-bf",
        "0",
        "-rc-lookahead",
        "0",
        "-spatial-aq",
        "0",
        "-temporal-aq",
        "0",
        "-c:a",
        "aac",
        "-b:a",
        "192k",
        ##########################
        # software encoding settings
        # "-c:v",
        # "libx264",
        # "-crf",
        # "28",
        # "-preset",
        # "fast",
        # "-c:a",
        # "aac",
        # "-b:a",
        # "192k",
    ],
}


def download_video(
    request: VideoDownloadRequest,
    convert_to_mp4: bool = False,
) -> None:
    if not request.output_path.exists():
        request.output_path.mkdir(exist_ok=True)

    YDL_OPTS.update(
        {
            "paths": {
                "home": str(request.output_path),
                "temp": str(request.temp_path),
            },
        }
    )
    if convert_to_mp4:
        YDL_OPTS.update(CONVERT_OPTS)

    with yt_dlp.YoutubeDL(YDL_OPTS) as ydl:
        ydl.download([request.url])


def video_downloader_worker(
    queue: list[VideoDownloadRequest],
    queue_lock: threading.RLock,
    convert_to_mp4: bool = False,
) -> None:
    while True:
        if not queue:
            time.sleep(2)
            continue

        with queue_lock:
            request = queue.pop(0)

        try:
            print(f"Starting download for {request.url} for user {request.user}")
            download_video(request, convert_to_mp4=convert_to_mp4)
            print(f"Completed download for {request.url} for user {request.user}")
        except Exception as e:
            print(f"Error downloading {request.url} for user {request.user}: {e}")


def test():
    # single video download test -> desktop
    download_video(
        VideoDownloadRequest(
            url="https://www.youtube.com/watch?v=vpTZWyOw_Uo",
            output_path=Path(r"C:\Users\timaevt\Desktop\temp"),
            temp_path=Path(r"C:\Users\timaevt\Desktop\temp\temp"),
            user="test_user",
        ),
        convert_to_mp4=True,
    )


if __name__ == "__main__":
    test()
