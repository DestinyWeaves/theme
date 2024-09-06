import logging
logging.basicConfig(level = logging.INFO)
log = logging.getLogger("")

import os
import subprocess
import re
import atexit
from selenium import webdriver
from selenium.webdriver.common.by import By
from jcink.adminpanel import AdminPanel
from jcink.filemanager import FileManager
from jcink.skinmanager import SkinManager
from jcink import skinupgrade

JCINK_ADMINURL=""
JCINK_USERNAME=""
JCINK_PASSWORD=""

wd = webdriver.Firefox()
driver = wd.__enter__()
atexit.register(wd.__exit__, None,None,None)

driver.set_page_load_timeout(20)
driver.implicitly_wait(0.1)

ap = AdminPanel(driver, JCINK_ADMINURL)
session = ap.login(JCINK_USERNAME, JCINK_PASSWORD)
session.__enter__()
atexit.register(session.__exit__, None,None,None)

fm = FileManager(ap)
sm = SkinManager(ap)

    
matches = sm.list_skins(skinupgrade.skin_name_regex)

upgrade_path = skinupgrade.calc_upgrade_path(matches)
