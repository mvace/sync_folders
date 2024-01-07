# The task is to create program that will synchronize two folders - source and replica, replica should match the content of source and get synchronized periodically
# all operations should be logged to a file and to the console
# folder paths, logfile path and sync interval should be provided using command line arguments

import os
import hashlib
import shutil
import logging

logger = logging.getLogger("sync_folders_logger")
logger.setLevel(logging.DEBUG)

file_handler = logging.FileHandler("log.log")
file_handler.setLevel(logging.DEBUG)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)

formatter = logging.Formatter("%(levelname)s - %(message)s")
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(console_handler)


def calculate_md5(path):
    md5 = hashlib.md5()

    for root, dirs, files in os.walk(path):
        relative_path = os.path.relpath(root, path)
        md5.update(relative_path.encode())

        for file_name in files:
            file_path = os.path.join(root, file_name)
            if os.path.isfile(file_path):
                with open(file_path, "rb") as file:
                    content = file.read()
                    md5.update(content)

    return md5.hexdigest()


source = r"C:\Users\marek\OneDrive\Plocha\Test\source"
replica = r"C:\Users\marek\OneDrive\Plocha\Test\replica"


print(f"SRC: {calculate_md5(source)} - REPLICA: {calculate_md5(replica)}")


# Loop through the files in source folder
# How to loop through both files and compare the files with the same name?
def sync_folders(source, replica):
    with os.scandir(source) as items:
        for item in items:
            file_name = item.name
            # rename these variables
            source_path = os.path.join(source, file_name)
            replica_path = os.path.join(replica, file_name)

            # checks if the file/folder exist in the replica folder
            if os.path.exists(replica_path):
                # checks if the files/folders are not identical
                if calculate_md5(replica_path) != calculate_md5(source_path):
                    # copy file to replica folder
                    if os.path.isfile(source_path):
                        shutil.copy2(source_path, replica)
                        logger.info(f"File '{file_name}' COPIED to {replica}")
                    # copy folder to replica folder
                    elif os.path.isdir(source_path):
                        shutil.rmtree(replica_path)
                        shutil.copytree(source_path, replica_path)
                        logger.info(f"Folder '{file_name}' COPIED to {replica}")

            # if file/folder does not exist in replica folder
            else:
                # copy file to replica folder
                if os.path.isfile(source_path):
                    shutil.copy2(source_path, replica)
                    # LOGGING - file CREATED at SOURCE
                    logger.info(f"File '{file_name}' CREATED at {source}")
                    # LOGGING - file COPIED to REPLICA
                    logger.info(f"File '{file_name}' COPIED to {replica}")
                # copy folder to replica folder
                elif os.path.isdir(source_path):
                    shutil.copytree(source_path, replica_path)
                    logger.info(f"Folder '{file_name}' CREATED at {source}")
                    # LOGGING - folder COPIED to REPLICA
                    logger.info(f"Folder '{file_name}' COPIED to {replica}")

    # Loop through the files in replica folder
    with os.scandir(replica) as items:
        for item in items:
            file_name = item.name
            source_path = os.path.join(source, file_name)
            replica_path = os.path.join(replica, file_name)

            # remove any redundant files/folders in the replica folder
            # log this operation into the logfile and to the console
            if not os.path.exists(source_path):
                if os.path.isfile(replica_path):
                    os.remove(replica_path)
                    # LOGGING - file REMOVED at SOURCE
                    logger.info(f"File '{file_name}' REMOVED at {source}")
                    # LOGGING - file REMOVED at REPLICA
                    logger.info(f"File '{file_name}' REMOVED at {replica}")
                elif os.path.isdir(replica_path):
                    shutil.rmtree(replica_path)
                    # LOGGING - folder REMOVED at SOURCE
                    logger.info(f"Folder '{file_name}' REMOVED at {source}")
                    # LOGGING - folder REMOVED at REPLICA
                    logger.info(f"Folder '{file_name}' REMOVED at {replica}")

    print(f"SRC: {calculate_md5(source)} - REPLICA: {calculate_md5(replica)}")


sync_folders(source, replica)

# schedule periodic synchronization
