from pathlib import Path
import shutil

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

for file in DOWNLOADS.iterdir():

    if file.is_dir():
        continue

    extension = file.suffix.lower()

    if extension in rules:
        destination_folder = DOWNLOADS / rules[extension]
    else:
        destination_folder = DOWNLOADS / "Miscellaneous"

        destination_folder.mkdir(exist_ok=True)

        shutil.move(
            str(file),
            str(destination_folder / file.name)
        )

        print(f"Moved: {file.name}")