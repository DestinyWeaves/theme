from selenium import webdriver
from jcink.adminpanel import AdminPanel
from jcink.filemanager import FileManager

admin_url="https://ajmansfieldtestboard.jcink.net/admin.php"
username="github_actions"
from getpass import getpass
password = getpass()

driver = webdriver.Chrome()
driver.set_page_load_timeout(1)
ap = AdminPanel(driver, admin_url)
sess = ap.login(username, password).__enter__()
fm = FileManager(ap)
    

    