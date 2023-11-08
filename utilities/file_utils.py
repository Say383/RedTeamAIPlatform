import os
import shutil
import logging

# Initialize the logger
logging.basicConfig(filename='file_utils.log', level=logging.INFO, format='%(asctime)s - %(levelname)s: %(message)s')

# Function to check if a file exists
def file_exists(file_path):
    try:
        return os.path.exists(file_path)
    except Exception as e:
        logging.error(f"Failed to check file existence. Error: {str(e)}")
        raise Exception("Failed to check file existence")

# Function to create a directory if it doesn't exist
def create_directory(directory_path):
    try:
        if not os.path.exists(directory_path):
            os.makedirs(directory_path)
            logging.info(f"Created directory: {directory_path}")
    except OSError as e:
        logging.error(f"Failed to create directory: {directory_path}. Error: {str(e)}")
        raise Exception(f"Failed to create directory: {directory_path}")

# Function to move a file to a different location
def move_file(source_path, destination_path):
    try:
        shutil.move(source_path, destination_path)
        logging.info(f"Moved file from {source_path} to {destination_path}")
    except FileNotFoundError:
        logging.error(f"File not found: {source_path}")
        raise Exception(f"File not found: {source_path}")
    except Exception as e:
        logging.error(f"Failed to move file. Error: {str(e)}")
        raise Exception(f"Failed to move file from {source_path} to {destination_path}")

# Function to delete a file
def delete_file(file_path):
    try:
        os.remove(file_path)
        logging.info(f"Deleted file: {file_path}")
    except FileNotFoundError:
        logging.error(f"File not found: {file_path}")
        raise Exception(f"File not found: {file_path}")
    except Exception as e:
        logging.error(f"Failed to delete file. Error: {str(e)}")
        raise Exception(f"Failed to delete file: {file_path}")

# Function to list files in a directory
def list_files(directory_path):
    try:
        files = os.listdir(directory_path)
        logging.info(f"Listed files in directory: {directory_path}")
        return files
    except FileNotFoundError:
        logging.error(f"Directory not found: {directory_path}")
        raise Exception(f"Directory not found: {directory_path}")
    except Exception as e:
        logging.error(f"Failed to list files. Error: {str(e)}")
        raise Exception(f"Failed to list files in directory: {directory_path}")

# Function to check if a file exists
def file_exists(file_path):
    try:
        return os.path.exists(file_path)
    except Exception as e:
        logging.error(f"Failed to check file existence. Error: {str(e)}")
        raise Exception("Failed to check file existence")

# Function to create a directory
def create_directory(directory_path):
    try:
        if not os.path.exists(directory_path):
            os.makedirs(directory_path)
        return directory_path
    except Exception as e:
        logging.error(f"Failed to create directory. Error: {str(e)}")
        raise Exception("Failed to create directory")

# Function to move a file to a different location
def move_file(source_path, destination_path):
    try:
        if file_exists(source_path):
            shutil.move(source_path, destination_path)
            logging.info(f"Moved file: {source_path} to {destination_path}")
        else:
            logging.error(f"Source file does not exist: {source_path}")
            raise Exception("Source file does not exist")
    except Exception as e:
        logging.error(f"Failed to move file. Error: {str(e)}")
        raise Exception("Failed to move file")

# Function to delete a file
def delete_file(file_path):
    try:
        if file_exists(file_path):
            os.remove(file_path)
            logging.info(f"Deleted file: {file_path}")
        else:
            logging.error(f"File does not exist: {file_path}")
            raise Exception("File does not exist")
    except Exception as e:
        logging.error(f"Failed to delete file. Error: {str(e)}")
        raise Exception("Failed to delete file")

