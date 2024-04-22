import os
import shutil
import datetime

class Backup:
    def __init__(self, main_path, backup_folder_path, exclude_dirs=None):
        self.main_path = main_path
        self.backup_folder_path = backup_folder_path
        self.exclude_dirs = exclude_dirs or []

    def backup(self):
        # Create the backup folder if it doesn't exist
        if not os.path.exists(self.backup_folder_path):
            os.makedirs(self.backup_folder_path)

        # Get current date and time
        current_datetime = datetime.datetime.now()

        log_messages = []
        log_message_start = f"Backup of {os.path.basename(self.main_path)} started at: {current_datetime}"
        log_messages.append(log_message_start)

        main_folder_name = os.path.basename(self.main_path)
        main_backup_path = os.path.join(self.backup_folder_path, main_folder_name + "_backup")
        os.makedirs(main_backup_path, exist_ok=True)

        # Walk through the desktop directory
        for root, dirs, files in os.walk(self.main_path):
            # Exclude specified directories
            for exclude_dir in self.exclude_dirs:
                if exclude_dir in dirs:
                    dirs.remove(exclude_dir)

            # Get relative path to the desktop
            relative_path = os.path.relpath(root, self.main_path)

            # Create corresponding directory structure in the backup folder
            backup_subfolder = os.path.join(main_backup_path, relative_path)
            os.makedirs(backup_subfolder, exist_ok=True)

            # Copy files to the backup folder
            for file in files:
                src_file = os.path.join(root, file)
                dest_file = os.path.join(backup_subfolder, file)
                shutil.copy2(src_file, dest_file)

        # Log completion
        completion_message = f"Backup of {os.path.basename(self.main_path)} completed at: {datetime.datetime.now()}"
        log_messages.append(completion_message)

        # Write log messages to a text file
        log_file_path = os.path.join("backup_log.txt")
        with open(log_file_path, "a") as log_file:
            for message in log_messages:
                log_file.write(message + "\n")
            log_file.write("\n")