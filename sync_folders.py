# The task is to create program that will synchronize two folders - source and replica, replica should match the content of source and get synchronized periodically
# all operations should be logged to a file and to the console
# folder paths, logfile path and sync interval should be provided using command line arguments

import os
import hashlib
import shutil


# Checks if files/folders are identical
def calculate_md5(path):
    md5 = hashlib.md5()

    for root, dirs, files in os.walk(path):
        # Include relative path in hash calculation
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
with os.scandir(source) as items:
    for item in items:
        file_name = item.name
        source_path = os.path.join(source, file_name)
        replica_path = os.path.join(replica, file_name)

        # checks if the file/folder exist in the replica folder
        if os.path.exists(replica_path):
            # checks if the files/folders are not identical
            if calculate_md5(replica_path) != calculate_md5(source_path):
                # copy file to replica folder
                if os.path.isfile(source_path):
                    shutil.copy2(source_path, replica)
                # copy folder to replica folder
                elif os.path.isdir(source_path):
                    shutil.rmtree(replica_path)
                    shutil.copytree(source_path, replica_path)

        # if file/folder does not exist in replica folder
        else:
            # copy file to replica folder
            if os.path.isfile(source_path):
                shutil.copy2(source_path, replica)
            # copy folder to replica folder
            elif os.path.isdir(source_path):
                shutil.copytree(source_path, replica_path)
            # log file creation into the logfile and to the console
            # log file copying into the logfile and to the console

            print(f"The file {file_name} was copied to the replica folder")

print(f"SRC: {calculate_md5(source)} - REPLICA: {calculate_md5(replica)}")
# Loop through the files in replica folder
## if there are any redundant files remove them
### log this operation into the logfile and to the console

# schedule periodic synchronization
