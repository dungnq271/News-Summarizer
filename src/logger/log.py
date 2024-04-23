import logging
import logging.config
from pathlib import Path

import yaml  # type: ignore

from src.utils import create_dir


def setup_logging(log_dir, config_fpath="logger_config.yml"):
    create_dir(log_dir)
    logging.getLogger("urllib3").setLevel(logging.WARNING)

    log_config = Path(config_fpath)
    if log_config.is_file():
        with open(log_config, "r") as f:
            config = yaml.safe_load(f.read())
            # modify logging paths based on log_dir
            for __, handler in config["handlers"].items():
                if "filename" in handler:
                    handler["filename"] = "/".join(
                        [log_dir, handler["filename"]]
                    )

        logging.config.dictConfig(config)
    else:
        logging.basicConfig(level=logging.INFO)
        print(
            f"Warning: logging configuration file is "
            f"not found in {log_config}."
        )


def setup_request_logging():
    import http.client

    http.client.HTTPConnection.debuglevel = 1

    # You must initialize logging, otherwise you'll not see debug output.
    logging.basicConfig()
    logging.getLogger().setLevel(logging.DEBUG)
    requests_log = logging.getLogger("requests.packages.urllib3")
    requests_log.setLevel(logging.DEBUG)
    requests_log.propagate = True


def get_logger(name):
    return logging.getLogger(name)
