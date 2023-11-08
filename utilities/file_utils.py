import os
import shutil
import logging

class FileUtils:
    def __init__(self):
        # Initialize the logger
        self.logger = logging.getLogger('file_utils')
        self.logger.setLevel(logging.INFO)
        handler = logging.FileHandler('file_utils.log')
        formatter = logging.Formatter('%(asctime)s - %(levelname)s: %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

    def file_exists(self, file_path):
        try:
            return os.path.exists(file_path)
        except OSError as e:
            self.logger.error(f"Failed to check file existence. Error: {str(e}")
            return False

    def create_directory(self, directory_path):
        try:
            if not os.path.exists(directory_path):
                os.makedirs(directory_path)
                self.logger.info(f"Created directory: {directory_path}")
        except OSError as e:
            self.logger.error(f"Failed to create directory: {directory_path}. Error: {str(e)}")
            raise Exception(f"Failed to create directory: {directory_path}")

    def move_file(self, source_path, destination_path):
        try:
            if self.file_exists(source_path):
                shutil.move(source_path, destination_path)
                self.logger.info(f"Moved file from {source_path} to {destination_path}")
            else:
                self.logger.error(f"Source file does not exist: {source_path}")
        except OSError as e:
            self.logger.error(f"Failed to move file. Error: {str(e)}")

    def delete_file(self, file_path):
        try:
            if self.file_exists(file_path):
                os.remove(file_path)
                self.logger.info(f"Deleted file: {file_path}")
            else:
                self.logger.error(f"File does not exist: {file_path}")
        except OSError as e:
            self.logger.error(f"Failed to delete file. Error: {str(e)}")

    def list_files(self, directory_path):
        try:
            files = os.listdir(directory_path)
            self.logger.info(f"Listed files in directory: {directory_path}")
            return files
        except OSError as e:
            self.logger.error(f"Failed to list files. Error: {str(e)}")
            raise Exception(f"Failed to list files in directory: {directory_path}")

if __name__ == "__main":
    file_utils = FileUtils()
    
    # Input your file and directory paths
    file_path = 'example.txt'
    directory_path = '~/RedTeamAIPlatform/'

    file_utils.create_directory(directory_path)
    file_utils.move_file(file_path, os.path.join(directory_path, os.path.basename(file_path)))
    file_utils.delete_file(file_path)
    files = file_utils.list_files(directory_path)
