# Python Backup Script

This Python script performs backups of a specified directory to another location. It can be useful for creating regular backups of important data.

## Features

- **Backup Functionality:** Automatically copies files from a specified directory to a backup folder.
- **Exclude Directories:** Allows excluding specific directories from the backup process.
- **Logging:** Logs the start and completion of each backup operation.

## Getting Started

### Prerequisites

- Python 3.x
- `os` and `shutil` libraries (usually included in Python standard library)

### Installation
Install the module using:
- **Windows**:
  - `pip install backupfolders`.
- **MacOs**:
  - `pip3 install backupfolders`.

### Usage
```python
from backupfolders import backupfolders

# source directory
mainPath = r"C:\Users\HP\Desktop\New folder (2)\flappy-bird"

# backup directory
destinationPath = r"D:\Backups"

# exclude folders not to backup
exclude_folders = [] #if any folder needs to be excluded from backup

backupdir = backupfolders.Backup()

backupdir.backup(mainPath, destinationPath, exclude_folders)

```

There will be a txt file created in which there will be backup log, of which folder you created backup and when it started and completed all this information

## Contributing
Contributions are welcome! If you find any issues or have suggestions for improvements, please open an issue or create a pull request

## License
This project is licensed under the MIT License.

## Acknowledgments
This script was inspired by the need for a simple backup solution.
Special thanks to the Python community for their valuable contributions and support.
