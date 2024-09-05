from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
import os

from contextlib import contextmanager

@contextmanager
def frame_selected(driver, frame: WebElement):
    driver.switch_to.frame(frame)
    try:
        yield
    finally:
        driver.switch_to.parent_frame()


