
import os

def split_lines(folder_name):
    for filename in os.listdir(os.path.join("data", folder_name)):
        with open(os.path.join("data", folder_name, filename), encoding="utf8") as f:
            lines = f.read().splitlines()
            for line in lines:
                yield line