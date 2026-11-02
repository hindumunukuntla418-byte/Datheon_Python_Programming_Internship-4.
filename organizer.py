
import os
import shutil
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(
    filename="organizer.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# File extension categories
FILE_CATEGORIES = {
    ".pdf": "Documents",
    ".doc": "Documents",
    ".docx": "Documents",
    ".txt": "Documents",
    ".ppt": "Documents",
    ".pptx": "Documents",
    ".xls": "Documents",
    ".xlsx": "Documents",

    ".jpg": "Images",
    ".jpeg": "Images",
    ".png": "Images",
    ".gif": "Images",
    ".bmp": "Images",

    ".mp4": "Videos",
    ".mkv": "Videos",
    ".avi": "Videos",
    ".mov": "Videos",

    ".zip": "Archives",
    ".rar": "Archives",
    ".7z": "Archives",
    ".tar": "Archives",

    ".py": "Code",
    ".java": "Code",
    ".html": "Code",
    ".css": "Code",
    ".js": "Code",
    ".cpp": "Code"
}


def get_category(file_path):
    """Identify the category using the file extension."""
    extension = file_path.suffix.lower()
    return FILE_CATEGORIES.get(extension, "Others")


def get_unique_path(destination):
    """Avoid overwriting files with the same name."""
    if not destination.exists():
        return destination

    counter = 1

    while True:
        new_name = (
            destination.stem
            + f"_{counter}"
            + destination.suffix
        )

        new_path = destination.with_name(new_name)

        if not new_path.exists():
            return new_path

        counter += 1


def organize_files(folder_path):
    """Organize files into category folders."""

    folder = Path(folder_path)

    if not folder.exists() or not folder.is_dir():
        print("Invalid folder path!")
        return

    # Get files before moving anything
    try:
        with os.scandir(folder) as entries:
            files = [
                Path(entry.path)
                for entry in entries
                if entry.is_file(follow_symlinks=False)
            ]
    except PermissionError:
        print("Permission denied: Cannot access this folder.")
        return

    total_files = len(files)
    moved_files = 0
    failed_files = 0

    print("\n====================================")
    print("       AUTOMATED FILE ORGANIZER")
    print("====================================")

    print("Total files found:", total_files)

    for file_path in files:
        category = get_category(file_path)

        destination_folder = folder / category

        try:
            # Create category folder if needed
            destination_folder.mkdir(exist_ok=True)

            destination = destination_folder / file_path.name

            # Handle duplicate filenames
            destination = get_unique_path(destination)

            # Move file
            shutil.move(str(file_path), str(destination))

            print(f"MOVED: {file_path.name} -> {category}")
            logging.info(
                "Moved %s to %s",
                file_path.name,
                destination
            )

            moved_files += 1

        except PermissionError:
            print(f"PERMISSION DENIED: {file_path.name}")
            logging.error("Permission denied: %s", file_path)

            failed_files += 1

        except OSError as error:
            print(f"ERROR: {file_path.name} - {error}")
            logging.error("Failed to move %s: %s", file_path, error)

            failed_files += 1

    print("\n====================================")
    print("          EXECUTION SUMMARY")
    print("====================================")

    print("Total files found:", total_files)
    print("Files successfully moved:", moved_files)
    print("Files failed:", failed_files)

    print("\nFile organization completed!")
    print("Check organizer.log for execution details.")


def main():
    print("\nWELCOME TO FILE ORGANIZER")

    folder_path = input(
        "\nEnter the folder path to organize: "
    ).strip().strip('"')

    if not folder_path:
        print("Folder path cannot be empty.")
        return

    folder = Path(folder_path).expanduser()

    if not folder.exists() or not folder.is_dir():
        print("Please enter a valid folder path.")
        return

    print("\nSelected folder:", folder.resolve())

    confirmation = input(
        "Do you want to organize this folder? (yes/no): "
    ).strip().lower()

    if confirmation in ("yes", "y"):
        organize_files(folder)
    else:
        print("Operation cancelled. No files were moved.")


if __name__ == "__main__":
    main()
