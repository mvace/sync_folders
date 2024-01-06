# The task is to create program that will synchronize two folders - source and replica, replica should match the content of source and get synchronized periodically
# all operations should be logged to a file and to the console
# folder paths, logfile path and sync interval should be provided using command line arguments

# Loop through the files in source folder
## check if they exist in the replica folder and if the size equals
### if no copy the file to the replica folder
### log file creation - with datetime
### log filey copying into the logfile and to the console

# Loop through the files in replica folder
## if there are any redundant files remove them
### log this operation into the logfile and to the console

# schedule periodic synchronization
