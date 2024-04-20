import os

import yaml  # type: ignore
from bs4 import NavigableString


def create_dir(dir_path):
    os.makedirs(dir_path, exist_ok=True)


def get_config(filepath):
    with open(filepath, "r") as f:
        config = yaml.safe_load(f)
    return config


def get_text_from_tag(tag):
    if isinstance(tag, NavigableString):
        return tag

    # else if isinstance(tag, Tag):
    return tag.text
