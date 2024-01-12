import os
import hashlib
import shutil
import logging
import argparse
import schedule
import time


def calculate_md5(path):
    # Calculate the MD5 hash of the given path (file or folder)
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


def sync_folders(source, replica, log, logger, initial=True):
    try:
        # Synchronize the contents of the source folder with the replica folder
        with os.scandir(source) as items:
            for item in items:
                file_name = item.name
                source_path = os.path.join(source, file_name)
                replica_path = os.path.join(replica, file_name)

                if os.path.exists(replica_path):
                    if calculate_md5(replica_path) != calculate_md5(source_path):
                        if os.path.isfile(source_path):
                            # If it's a file, copy it to the replica folder
                            shutil.copy2(source_path, replica)
                            logger.info(f"File '{file_name}' COPIED to {replica}")

                        elif os.path.isdir(source_path):
                            # If it's a folder, remove the existing replica folder and copy the source folder
                            shutil.rmtree(replica_path)
                            shutil.copytree(source_path, replica_path)
                            logger.info(f"Folder '{file_name}' COPIED to {replica}")

                else:
                    # If the item does not exist in the replica folder, copy it
                    if os.path.isfile(source_path):
                        shutil.copy2(source_path, replica)
                        if not initial:
                            logger.info(f"File '{file_name}' CREATED at {source}")
                        logger.info(f"File '{file_name}' COPIED to {replica}")

                    elif os.path.isdir(source_path):
                        shutil.copytree(source_path, replica_path)
                        if not initial:
                            logger.info(f"Folder '{file_name}' CREATED at {source}")
                        logger.info(f"Folder '{file_name}' COPIED to {replica}")

        # Check for items in the replica folder that do not exist in the source folder and remove them
        with os.scandir(replica) as items:
            for item in items:
                file_name = item.name
                source_path = os.path.join(source, file_name)
                replica_path = os.path.join(replica, file_name)

                if not os.path.exists(source_path):
                    if os.path.isfile(replica_path):
                        os.remove(replica_path)
                        logger.info(f"File '{file_name}' REMOVED at {source}")
                        logger.info(f"File '{file_name}' REMOVED at {replica}")

                    elif os.path.isdir(replica_path):
                        shutil.rmtree(replica_path)
                        logger.info(f"Folder '{file_name}' REMOVED at {source}")
                        logger.info(f"Folder '{file_name}' REMOVED at {replica}")

    except Exception as e:
        # Log any errors that occur during synchronization
        logger.error(f"Error during synchronization: {str(e)}")


def main():
    # Set up command-line argument parser
    parser = argparse.ArgumentParser(
        description="A synchronization tool that ensures the replica folder mirrors the contents of the source folder, maintaining a complete and identical copy of the source directory."
    )
    parser.add_argument(
        "source",
        metavar="source",
        type=str,
        help="Enter the path to a source folder you want to synchronize",
    )
    parser.add_argument(
        "replica",
        metavar="replica",
        type=str,
        help="Enter the path to a replica folder for synchronization",
    )
    parser.add_argument(
        "log",
        metavar="log",
        type=str,
        help="Enter the path where to store the log file. Make sure it is not the path to the source or replica folder you want to synchronize",
    )
    parser.add_argument(
        "interval",
        metavar="interval",
        type=float,
        help="Enter interval in seconds in which you want to run the synchronization",
    )

    args = parser.parse_args()
    source = os.path.abspath(args.source)
    replica = os.path.abspath(args.replica)
    log = os.path.abspath(args.log)
    interval = args.interval

    # Set up logger configuration
    logger = logging.getLogger("sync_folders_logger")
    logger.setLevel(logging.DEBUG)

    # Check if handlers already exist to avoid duplicate log entries
    if not logger.handlers:
        log_path = os.path.join(log, "log.log")
        file_handler = logging.FileHandler(log_path)
        file_handler.setLevel(logging.DEBUG)

        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)

        formatter = logging.Formatter("%(levelname)s - %(message)s")
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)

        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

    if log == source or log == replica:
        raise ValueError(
            "The log path must be different from the source and replica paths."
        )

    if source == replica:
        raise ValueError("The source path must be different from the replica path")

    # Initial synchronization
    sync_folders(source, replica, log, logger)

    # Schedule periodic synchronization
    schedule.every(interval).seconds.do(
        lambda: sync_folders(source, replica, log, logger, initial=False)
    )

    # Run the scheduler loop
    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == "__main__":
    main()
