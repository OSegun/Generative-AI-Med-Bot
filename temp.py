import os, logging
from pathlib import Path


logging.basicConfig(level=logging.INFO, format='[%(asctime)s]: %(message)s:')

files = [
    "resource/__init__.py",
    "resource/helper.py",
    "resource/prompt.py",
    ".env",
    "setup.py",
    "app.py",
    "test/test.ipynb",
    "test.py"
]

for file_path in files:
    file_path = Path(file_path)
    file_dir, file_name = os.path.split(file_path)


    if file_dir != "":
        os.makedirs(file_dir, exist_ok=True)
        logging.info(f"Creating directory; {file_dir} for the file: {file_name}")

    if (not os.path.exists(file_path)) or (os.path.getsize(file_path) == 0):
        with open(file_path, "w") as f:
            pass
            logging.info(f"Creating empty file: {file_path}")

    else:
        logging.info(f"{file_name} already exist")