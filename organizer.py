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

        # ❌ Ignore incomplete downloads
        if file.suffix.lower() in [".tmp", ".crdownload", ".part"]:
            return

        extension = file.suffix.lower()

        # Decide folder
        if extension in rules:
            destination_folder = DOWNLOADS / rules[extension]
        else:
            destination_folder = DOWNLOADS / "Miscellaneous"

        # Create folder if not exists
        destination_folder.mkdir(exist_ok=True)

        # ✅ Wait for file to finish writing
        time.sleep(2)

        # ❌ If file disappeared, skip
        if not file.exists():
            return

        try:
            shutil.move(
                str(file),
                str(destination_folder / file.name)
            )

            print(f"Moved: {file.name} -> {destination_folder.name}")

        except FileNotFoundError:
            print(f"Skipped (still downloading): {file.name}")

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