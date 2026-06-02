from pathlib import Path
import shutil
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time

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


class DownloadHandler(FileSystemEventHandler):

    def on_created(self, event):

        if event.is_directory:
            return

        file = Path(event.src_path)

        extension = file.suffix.lower()

        # Decide destination folder
        if extension in rules:
            destination_folder = DOWNLOADS / rules[extension]
        else:
            destination_folder = DOWNLOADS / "Miscellaneous"

        # Create folder if it doesn't exist
        destination_folder.mkdir(exist_ok=True)

        # Small delay so file is fully downloaded
        time.sleep(1)

        try:
            shutil.move(
                str(file),
                str(destination_folder / file.name)
            )

            print(f"Moved: {file.name} -> {destination_folder.name}")

        except Exception as e:
            print(f"Error moving {file.name}: {e}")


observer = Observer()

observer.schedule(
    DownloadHandler(),
    str(DOWNLOADS),
    recursive=False
)

observer.start()

print("Monitoring Downloads folder... (Press Ctrl + C to stop)")

try:
    while True:
        time.sleep(1)

except KeyboardInterrupt:
    observer.stop()

observer.join()