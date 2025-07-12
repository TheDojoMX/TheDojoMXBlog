"""File backup utilities for Voice Papers."""

import shutil
from pathlib import Path
from datetime import datetime


def backup_existing_file(file_path: Path) -> bool:
    """
    Backup an existing file by moving it to a backup folder with timestamp.

    Args:
        file_path: Path to the file to backup

    Returns:
        True if backup was created, False if file didn't exist
    """
    if not file_path.exists():
        return False

    # Create backup directory
    backup_dir = file_path.parent / "backups"
    backup_dir.mkdir(exist_ok=True)

    # Generate timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # Create backup filename
    backup_name = f"{file_path.stem}_{timestamp}{file_path.suffix}"
    backup_path = backup_dir / backup_name

    # Move file to backup
    shutil.move(str(file_path), str(backup_path))

    return True


def get_filename_with_focus(base_name: str, focus: str, extension: str = None) -> str:
    """
    Generate filename with focus mode included.

    Args:
        base_name: Base filename (with or without extension)
        focus: Focus mode (e.g., "explanatory", "critical")
        extension: Optional extension to use (e.g., ".txt", ".mp3"). If not provided,
                  will use extension from base_name if present, otherwise defaults to .txt

    Returns:
        Filename with focus mode included
    """
    # Split the base name and extension
    path = Path(base_name)
    name_without_ext = path.stem

    # Determine the extension to use
    if extension is not None:
        # Use the provided extension
        final_extension = extension if extension.startswith(".") else f".{extension}"
    elif path.suffix:
        # Use the extension from base_name
        final_extension = path.suffix
    else:
        # Default to .txt if no extension provided
        final_extension = ".txt"

    if focus:
        result = f"{name_without_ext}_{focus}{final_extension}"
        return result

    result = f"{name_without_ext}{final_extension}"
    return result
