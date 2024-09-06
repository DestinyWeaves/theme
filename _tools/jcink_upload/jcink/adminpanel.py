from selenium import webdriver
from selenium.webdriver.common.by import By
import time

from contextlib import contextmanager

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

        self.driver.switch_to.frame(self.menu_frame)
        self.driver.find_element(By.LINK_TEXT, "Expand").click()
        self.driver.switch_to.parent_frame()

        self.driver.switch_to.frame(self.body_frame) # while logged in, we are implicitly in the body frame
        try:
            yield self
        finally:
            self.driver.switch_to.parent_frame()
            # TODO explicitly sign out of the admin session
            # self.driver.get(f"https://{hostname}/index.php")
            # logout_link = self.driver.find_element(by=By.CSS_SELECTOR, value="#log-out")
            # logout_link.click()
    
    def nav_to_section(self, page:str):
        self.driver.switch_to.parent_frame() # switch out of body_frame
        self.driver.switch_to.frame(self.menu_frame)
        self.driver.find_element(By.LINK_TEXT, page).click()
        time.sleep(0.1)
        self.driver.switch_to.parent_frame()
        self.driver.switch_to.frame(self.body_frame) # back to body_frame
    
