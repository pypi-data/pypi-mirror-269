import time
from concurrent.futures import ThreadPoolExecutor
from threading import RLock, Lock

import logging
log = logging.getLogger(__name__)
st = logging.StreamHandler()
log.setLevel(logging.DEBUG)
fmt = logging.Formatter("%(asctime)s [%(levelname)s] %(name)s (%(threadName)s): %(message)s")
st.setFormatter(fmt)
log.addHandler(st)

class Test:

    def __init__(self):

        self.lock = RLock()

    def sleep(self):
        with self.lock:
            log.info("Sleeping")
            time.sleep(1)
            log.info("Woke up")

    def t1(self):
        with ThreadPoolExecutor(max_workers=1) as executor:
            executor.submit(self.sleep)

    def run(self):
        with ThreadPoolExecutor(max_workers=10) as executor:
            for i in range(10):
                executor.submit(self.t1)


if __name__ == "__main__":
    Test().run()


