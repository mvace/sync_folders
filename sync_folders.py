# The task is to create program that will synchronize two folders - source and replica, replica should match the content of source and get synchronized periodically
# all operations should be logged to a file and to the console
# folder paths, logfile path and sync interval should be provided using command line arguments

import os
import hashlib
import shutil
import logging
import argparse
import schedule
import time


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


def sync_folders(
    source,
    replica,
    log,
    logger,
    initial=True,
):
    with os.scandir(source) as items:
        for item in items:
            file_name = item.name
            # rename these variables
            source_path = os.path.join(source, file_name)
            replica_path = os.path.join(replica, file_name)

            if os.path.exists(replica_path):
                if calculate_md5(replica_path) != calculate_md5(source_path):
                    if os.path.isfile(source_path):
                        shutil.copy2(source_path, replica)
                        logger.info(f"File '{file_name}' COPIED to {replica}")

                    elif os.path.isdir(source_path):
                        shutil.rmtree(replica_path)
                        shutil.copytree(source_path, replica_path)
                        logger.info(f"Folder '{file_name}' COPIED to {replica}")

            else:
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


def main():
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
        help="Enter the path to a replica folder for synchrozization",
    )

    parser.add_argument(
        "log",
        metavar="log",
        type=str,
        help="Enter the path where to store the log file. Make sure it is not the path to source or replica folder you want to synchronize",
    )

    args = parser.parse_args()
    source = rf"{args.source}"
    replica = rf"{args.replica}"
    log = rf"{args.log}"

    logger = logging.getLogger("sync_folders_logger")
    logger.setLevel(logging.DEBUG)

    log_path = rf"{log}\log.log"
    file_handler = logging.FileHandler(log_path)
    file_handler.setLevel(logging.DEBUG)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)

    formatter = logging.Formatter("%(levelname)s - %(message)s")
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    if log == source or log == source:
        raise ValueError(
            "The log path must be different from the source and replica paths."
        )
    # print(f"SRC: {calculate_md5(source)} - REPLICA: {calculate_md5(replica)}")
    sync_folders(source, replica, log, logger)
    schedule.every(15).seconds.do(
        lambda: sync_folders(source, replica, log, logger, initial=False)
    )

    while True:
        schedule.run_pending()
        time.sleep(1)
        # print(f"SRC: {calculate_md5(source)} - REPLICA: {calculate_md5(replica)}")

    # schedule periodic synchronization


if __name__ == "__main__":
    main()
