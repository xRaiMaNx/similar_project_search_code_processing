import logging

LOGGER = logging.getLogger("main_logger")
LOGGER.setLevel(logging.DEBUG)
sh = logging.StreamHandler()
sh.setLevel(logging.DEBUG)
# formatter = logging.Formatter("[%(asctime)s] %(levelname)s: %(message)s",
#                               "%Y-%m-%d %H:%M:%S")
formatter = logging.Formatter("[%(asctime)s] %(levelname)s: %(message)s", "%Y-%m-%d %H:%M:%S")
sh.setFormatter(formatter)
LOGGER.addHandler(sh)
