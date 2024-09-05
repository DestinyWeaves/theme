import argparse
import logging
logging.basicConfig(level = logging.INFO)
log = logging.getLogger("")

import os
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from jcink.adminpanel import AdminPanel
from jcink.filemanager import FileManager
from jcink.skinmanager import SkinManager

def environ_or_required(key):
    return (
        {'default': os.environ.get(key)} if os.environ.get(key)
        else {'required': True}
    )
parser = argparse.ArgumentParser(
    prog="JCINK Uploader",
    description="Automate updating a skinpack through the JCINK Admin Panel",
)
parser.add_argument('--skin', action='append')
parser.add_argument('--assets')
parser.add_argument('--assets-root', default=os.curdir)
parser.add_argument('--admin-url', **environ_or_required('JCINK_ADMINURL'))
parser.add_argument('--admin-user', **environ_or_required('JCINK_USERNAME'))
parser.add_argument('--admin-pass', **environ_or_required('JCINK_PASSWORD'))
parser.add_argument('--remote-driver', default=None) # http://127.0.0.1:4444/wd/hub
args = parser.parse_args()


def fully_split_path(winpath:str):
    components = []
    while winpath:
        winpath, component = os.path.split(winpath)
        components.insert(0, component)
    return components

if args.remote_driver:
    wd = webdriver.Remote(
        command_executor=args.remote_driver,
        options=webdriver.FirefoxOptions(),
    )
else:
    wd = webdriver.Firefox()

with wd as driver:
    driver.set_page_load_timeout(10)
    driver.implicitly_wait(1)
    ap = AdminPanel(driver, args.admin_url)
    fm = FileManager(ap)
    sm = SkinManager(ap)

    with ap.login(args.admin_user, args.admin_pass):
        for root, dirs, files in os.walk(args.assets):
            src_root = os.path.abspath(root)
            dst_root = "/" + "/".join(fully_split_path(os.path.relpath(root, args.assets_root)))

            log.info("mkdir %s -> %s", src_root, dst_root)
            try:
                fm.mkdir(dst_root)
            except FileExistsError:
                log.warning("folder already exists")
            for file in files:
                src_file = os.path.join(src_root, file)
                dst_file = "/".join((dst_root, file))
                log.info("upload %s -> %s", src_file, dst_file)
                fm.upload_file(src_file, dst_root)
        
        for skin in args.skin:
            sm.create_new(skin)
    