import logging
log = logging.getLogger("fm")
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import InvalidSelectorException, NoSuchElementException, StaleElementReferenceException
import os
import errno
from .frame import frame_selected
from .adminpanel import AdminPanel


class SkinManager:
    def __init__(self, ap: AdminPanel):
        self.driver = ap.driver
        self.ap = ap

    def nav(self):
        self.ap.nav_to_section("Manage Skin Sets")
    
    def create_new(self, skinset_file):
        self.nav()
        with frame_selected(self.driver, self.ap.body_frame):
            while True:
                form = self.driver.find_element(By.NAME, "uploadform")
                try:
                    form.find_element(By.NAME, "FILE_UPLOAD").send_keys(os.path.abspath(skinset_file))
                except StaleElementReferenceException:
                    continue
                break
            form.find_element(By.CSS_SELECTOR, "#button").click()

            result_text = self.driver.find_element(By.CSS_SELECTOR, "#description").text
        log.info("result %s", result_text)
        if result_text != "The action was executed successfully":
            raise Exception(result_text)