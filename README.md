# Folder Synchronization Tool

This Python script is a synchronization tool that ensures the replica folder mirrors the contents of the source folder, maintaining a complete and identical copy of the source directory.

## Features

- **Synchronization:** Keeps the source and replica folders in sync.
- **MD5 Hash Check:** Uses MD5 hash comparison to identify changes.
- **Logging:** Detailed logging of synchronization actions.
- **Periodic Synchronization:** Allows you to set an interval for automatic synchronization.



## Installation

To run the project locally, follow these steps:

#### 1. Clone the repository:

   ```bash
   git clone https://github.com/mvace/sync_folders
   ```


#### 2. Navigate to the project directory:

```bash
cd sync_folders
```

#### 3. Create and Activate a Virtual Environment

```bash
python -m venv venv
```
#### On Windows:
```bash
.\venv\Scripts\activate
```

#### On macOS and Linux:
```bash
source venv/bin/activate
```

#### 4. Install dependencies:

```bash
pip install -r requirements.txt
```

#### 5. Run the Script:

```bash
python sync_folders.py source_folder replica_folder log_folder interval_in_seconds
```
**source_folder:** Path to the source folder you want to synchronize.

**replica_folder:** Path to the replica folder for synchronization.

**log_folder:** Path to store the log file (not the source or replica folder).

**interval_in_seconds:** Interval in seconds for periodic synchronization.

#### Example:

```bash
python sync_folders.py C:\path\to\source C:\path\to\replica C:\path\to\log 30
```

#### Configuration
Ensure that the log folder is different from the source and replica folders.
Ensure that replica and source folder paths are different

