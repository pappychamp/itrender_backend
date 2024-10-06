import logging

logger = logging.getLogger()


st_handler = logging.StreamHandler()
formatter = logging.Formatter("%(asctime)s - %(filename)s:%(lineno)d - %(levelname)s - %(message)s")
st_handler.setFormatter(formatter)
logger.addHandler(st_handler)
logger.setLevel(logging.INFO)
