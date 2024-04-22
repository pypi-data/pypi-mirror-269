# Python Backup Script

This Python script performs backups of a specified directory to another location. It can be useful for creating regular backups of important data.

## Features

- **Backup Functionality:** Automatically copies files from a specified directory to a backup folder.
- **Exclude Directories:** Allows excluding specific directories from the backup process.
- **Logging:** Logs the start and completion of each backup operation, including any errors encountered.

## Getting Started

### Prerequisites

- Python 3.x
- `os` and `shutil` libraries (usually included in Python standard library)

### Installation

1. Clone this repository to your local machine.
2. Ensure you have Python installed.
3. Navigate to the directory where the script is located.

### Usage

1. Open the `backup.py` script.
2. Modify the `main_path`, `backup_folder_path`, and `exclude_dirs` variables to suit your needs.
3. Run the script using Python: `python backup.py`.

### Example

```python
from backupfolders import Backup

# Define main path and backup folder path
main_path = "/path/to/source/directory"
backup_folder_path = "/path/to/backup/directory"

# Create an instance of the Backup class
backup_instance = Backup(main_path, backup_folder_path)

# Perform the backup
backup_instance.backup()