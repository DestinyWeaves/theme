from selenium import webdriver
from selenium.webdriver.common.by import By

from contextlib import contextmanager
from .frame import frame_selected

class AdminPanel:
    def __init__(self, driver:webdriver.Chrome, admin_url:str):
        self.driver = driver
        self.admin_url = admin_url

    @contextmanager
    def login(self, username, password):
        self.driver.get(self.admin_url)
        self.driver.find_element(by=By.NAME, value="username").send_keys(username)
        self.driver.find_element(by=By.NAME, value="password").send_keys(password)
        self.driver.find_element(by=By.CSS_SELECTOR, value="#button").click()

        self.menu_frame = self.driver.find_element(By.NAME, "menu")
        self.body_frame = self.driver.find_element(By.NAME, "body")
        with frame_selected(self.driver, self.menu_frame):
            self.driver.find_element(By.LINK_TEXT, "Expand").click()

        try:
            yield self
        finally:
            pass
            # TODO explicitly sign out of the admin session
            # self.driver.get(f"https://{hostname}/index.php")
            # logout_link = self.driver.find_element(by=By.CSS_SELECTOR, value="#log-out")
            # logout_link.click()
    
    def nav_to_section(self, page:str):
        with frame_selected(self.driver, self.menu_frame):
            self.driver.find_element(By.LINK_TEXT, page).click()
    
