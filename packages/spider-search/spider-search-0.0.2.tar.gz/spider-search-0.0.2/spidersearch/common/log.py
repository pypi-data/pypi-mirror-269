import logging

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(levelname)s %(filename)s:%(lineno)d %(message)s',
                    datefmt='%Y-%d-%m %H:%M:%S')
logger = logging.getLogger(__file__)
