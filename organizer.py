from pathlib import Path
import shutil
import time
import threading

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

import pystray
from pystray import MenuItem as item
from PIL import Image, ImageDraw


# ================= CONFIG =================
DOWNLOADS = Path.home() / "Downloads"

rules = {
    ".pdf": "Documents",
    ".zip": "Archives",
    ".rar": "Archives",
    ".png": "Images",
    ".jpg": "Images",
    ".jpeg": "Images",
    ".gif": "Images",
    ".mp4": "Videos",
    ".mkv": "Videos",
    ".exe": "Installers",
    ".iso": "ISOs"
}

paused = False


# ================= HANDLER =================
class DownloadHandler(FileSystemEventHandler):

    def on_created(self, event):

        global paused

        if paused:
            return

        if event.is_directory:
            return

        file = Path(event.src_path)

        # ignore incomplete downloads
        if file.suffix.lower() in [".tmp", ".crdownload", ".part"]:
            return

        extension = file.suffix.lower()

        if extension in rules:
            destination_folder = DOWNLOADS / rules[extension]
        else:
            destination_folder = DOWNLOADS / "Miscellaneous"

        destination_folder.mkdir(exist_ok=True)

        time.sleep(2)

        if not file.exists():
            return

        try:
            shutil.move(
                str(file),
                str(destination_folder / file.name)
            )
            print(f"Moved: {file.name}")

        except Exception as e:
            print(f"Error: {e}")


# ================= WATCHDOG =================
observer = Observer()
observer.schedule(DownloadHandler(), str(DOWNLOADS), recursive=False)


def start_watching():
    observer.start()
    observer.join()


# ================= SYSTEM TRAY =================
def create_image():
    return Image.open("icons\down_arrow.jpg")

def on_pause(icon, item):
    global paused
    paused = True
    print("Paused")


def on_resume(icon, item):
    global paused
    paused = False
    print("Resumed")


def on_exit(icon, item):
    observer.stop()
    icon.stop()


icon = pystray.Icon(
    "Download Organizer",
    create_image(),
    "Download Organizer",
    menu=pystray.Menu(
        item("Pause", on_pause),
        item("Resume", on_resume),
        item("Exit", on_exit)
    )
)


# ================= RUN =================
threading.Thread(target=start_watching, daemon=True).start()

icon.run()