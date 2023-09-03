import logging


log = logging
log.basicConfig(level=logging.INFO,
                filename='logs.log',
                filemode="a+",
                format="%(asctime)s %(levelname)s %(message)s")
