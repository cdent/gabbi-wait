
import os
import sys
import tty
import termios

from gabbi import driver
from gabbi import handlers


def getch():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch


class WaitResponseHandler(handlers.ResponseHandler):

    test_key_suffix = 'wait'
    test_key_value = {}

    def action(self, test, key, value):
        while True:
            char = getch()
            if char == value:
                break


def load_tests(loader, tests, pattern):
    """Provide a TestSuite to the discovery process."""
    # Set and environment variable for one of the tests.
    test_dir = os.path.join(os.path.dirname(__file__), 'gabbits')
    return driver.build_tests(test_dir, loader, host='localhost',
                              response_handlers=[WaitResponseHandler])
