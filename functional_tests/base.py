from selenium import webdriver
from django.contrib.staticfiles.testing import LiveServerTestCase
from selenium.common.exceptions import WebDriverException
from datetime import datetime
import time
import os

MAX_WAIT = 10

SCREEN_DUMP_LOCATION = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), 'screendumps'
)


def test():
    # print(__file__)
    # print(os.path.abspath(__file__))
    # print(os.path.dirname(os.path.abspath(__file__)))
    # print(SCREEN_DUMP_LOCATION)
    # timestamp = datetime.now().isoformat().replace(':', '.')[:19]
    # print(datetime.now())
    # print(datetime.now().isoformat())
    # print(datetime.now().isoformat().replace(':', '.')[:19])

    # ft = FunctionalTest()

    # print('{folder}/{classname}.{method}-{timestamp}'.format(
    #     folder=SCREEN_DUMP_LOCATION,
    #     classname=ft.__class__.__name__,
    #     method=ft._testMethodName,
    #     timestamp=timestamp)
    # )
    pass


def wait(fn):
    def modified_fn(*args, **kwargs):
        start_time = time.time()
        while True:
            try:
                return fn(*args, **kwargs)
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT:
                    raise e
                else:
                    time.sleep(0.5)

    return modified_fn


class FunctionalTest(LiveServerTestCase):

    @wait
    def wait_for(self, fn):
        return fn()

    def take_screenshot(self):
        filename = self._get_filename() + '.png'
        print('screenshotting to', filename)
        self.browser.get_screenshot_as_file(filename)

    def _get_filename(self):
        timestamp = datetime.now().isoformat().replace(':', '.')[:19]
        return '{folder}/{classname}.{method}-window{windowid}-{timestamp}'.format(
            folder=SCREEN_DUMP_LOCATION,
            classname=self.__class__.__name__,
            method=self._testMethodName,
            windowid=self._windowid,
            timestamp=timestamp
        )


if __name__ == '__main__':
    test()
