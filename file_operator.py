from pathlib import Path


def init_folders(temp_dir: Path, base_dir: Path, users: list[str]):
    temp_dir.mkdir(exist_ok=True)
    base_dir.mkdir(exist_ok=True)
    for user in users:
        (base_dir / user).mkdir(exist_ok=True)


def init_txt_files(base_dir: Path, users: list[str], erase_existing=False):
    for user in users:
        txt_file = base_dir / f"{user}.txt"
        if erase_existing and txt_file.exists():
            txt_file.unlink()
        if not txt_file.exists():
            txt_file.touch()


def check_filesize_changed(path: Path, previous_size: int = -1) -> bool:
    current_size = path.stat().st_size
    if current_size == previous_size:
        print("File size stable:", path)
        print("Final size (bytes):", current_size)
        return False
    else:
        print("File size changed, waiting...", path)
        print("Final size (bytes):", current_size)
        return True


def read_and_erase_request_file(path: Path) -> list[str]:
    with open(path, "r") as f:
        lines = f.readlines()

    with open(path, "w") as f:
        f.write("")

    if lines:
        return [line.strip() for line in lines if line.strip()]
    return []
