import os
import shutil
import logging

if not os.path.exists("logs"):
    os.mkdir("logs")

logging.basicConfig(
    level=logging.INFO, 
    format="%(asctime)s %(levelname)s: %(message)s",
    filename="logs/log.log",
    filemode="w"
)

def copy_static(source, destination):
    if os.path.exists(destination):
        logging.info(f"Removing destination: {destination}")
        shutil.rmtree(destination)
    logging.info(f"Creating destination: {destination}")
    os.mkdir(destination)
    copy_static_r(source, destination)

def copy_static_r(source, destination): #recursive helper function
    contents = os.listdir(source)
    for item in contents:
        file_path = os.path.join(source, item)
        if not os.path.isfile(file_path):
            new_destination = os.path.join(destination, item)
            logging.info(f"Creating directory: {new_destination}")
            os.mkdir(new_destination)
            copy_static_r(file_path, new_destination)
        else:
            logging.info(f"Copying file: {file_path}")
            shutil.copy(file_path, destination)