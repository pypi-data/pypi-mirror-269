from dataclasses import dataclass
import time
import ctypes
from termcolor import colored
import sys


def countdown(text, mins):
    t = mins
    while t > 0:
        timer = ' - {:02d} mins left'.format(t)
        print('\r' + text + colored(timer, 'green'), end='')
        time.sleep(1)
        t -= 1

    if sys.platform == "win32":
        ctypes.windll.user32.FlashWindow(ctypes.windll.kernel32.GetConsoleWindow(), True)

    input(f"\r{text} - Time up, carry on?")


@dataclass
class SpecialPrompt:
    text: str
    durationMins: int

    def show(self):
        countdown(self.text, self.durationMins)


SPECIAL_PROMPTS = [
    SpecialPrompt('Strategy Time', 15),
    SpecialPrompt('Mail and slack', 2)
]
