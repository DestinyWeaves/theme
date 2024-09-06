import logging
log = logging.getLogger("fm")
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import InvalidSelectorException, NoSuchElementException, StaleElementReferenceException
import os
import errno
import time
from .adminpanel import AdminPanel


class FileManager:
    def __init__(self, ap: AdminPanel):
        self.driver = ap.driver
        self.ap = ap

    def cd_single(self, component:str):
        if component == "": # i.e. begin component was /
            log.debug("nav to file manager page")
            self.ap.nav_to_section("File Manager")
        else:
            log.debug("nav to %s", component)
            while True:
                table = self.driver.find_element(By.CSS_SELECTOR, "#acp_form .tableborder")
                try:
                    table.find_element(By.LINK_TEXT, component).click()
                except StaleElementReferenceException:
                    continue
                except InvalidSelectorException as e:
                    raise FileNotFoundError(component) from e
                break

    def cd(self, path:str):
        log.debug("cd %s", path)
        components = path.split('/')
        for component in components:
            self.cd_single(component)
    
    def mkdir(self, path:str, parents=False):
        if parents:
            log.debug("mkdir -p %s", path)
            self.mkdir_parents(path)
        elif path == "":
            pass
        else:
            log.debug("mkdir %s", path)
            dirname, name = path.rsplit('/', 1)
            self.cd(dirname)

            log.debug("create dir %s", name)

            while True:
                form = self.driver.find_element(By.NAME, "uploadform")
                try:
                    form.find_element(By.NAME, "folder_name").send_keys(name)
                except StaleElementReferenceException:
                    continue
                break
            form.find_element(By.CSS_SELECTOR, "#button").click()

            result_text = self.driver.find_element(By.CSS_SELECTOR, ".tdrow1").text
            log.debug("result %s", result_text)

            if "already exists" in result_text:
                raise FileExistsError(result_text)
        
    def mkdir_parents(self, path:str):
        components = path.split("/")
        path = ""
        for component in components:
            path = path + "/" + component
            try:
                self.mkdir(path, parents=False)
            except FileExistsError:
                pass
    
    def rm(self, path:str, file=True, dir=True, dry_run=False):
        log.debug("rm %s", path)
        if file and dir:
            checkbox_query = (By.CSS_SELECTOR, "input[type=checkbox]")
        elif file and not dir:
            checkbox_query = (By.NAME, "rm_folders[]")
        elif dir and not file:
            checkbox_query = (By.NAME, "rm_files[]")
        else:
            raise ValueError("must select at least one of: file, dir")

        dirname, name = path.rsplit('/', 1)
        self.cd(dirname)

        while True:
            table = self.driver.find_element(By.CSS_SELECTOR, "#acp_form .tableborder")
            try:
                label = table.find_element(By.LINK_TEXT, name) # <a> element
            except StaleElementReferenceException:
                continue
            except NoSuchElementException as e:
                raise FileNotFoundError(path) from e
            break
        row = label.find_element(By.XPATH,"../..") 
        checkbox = row.find_element(*checkbox_query)
        checkbox.click()

        del_button = table.find_element(By.CSS_SELECTOR, 'input[value="Delete"]')
        if dry_run:
            log.info("dry_run, would delete %s", path)
            return
        del_button.click()

        result_text = self.driver.find_element(By.CSS_SELECTOR, "#description").text
        log.debug("result %s", result_text)
        if result_text != "The action was executed successfully":
            raise Exception(result_text)
        
    def rm_contents(self, path:str, dry_run=False):
        log.debug("rm %s/**", path)

        self.cd(path)

        subfolder_checks = self.driver.find_elements(By.NAME, "rm_folders[]")
        if subfolder_checks:
            subfolder_rows = [check.find_element(By.XPATH, "../../..") for check in subfolder_checks]
            subfolder_names = [row.find_element(By.TAG_NAME, "a").text for row in subfolder_rows]

            for name in subfolder_names:
                self.rm_contents(path + "/" + name, dry_run=dry_run)
            
            self.cd(path)
        
        subfolder_checks = self.driver.find_elements(By.NAME, "rm_folders[]")
        for check in subfolder_checks:
            check.click()
        file_checks = self.driver.find_elements(By.NAME, "rm_files[]")
        for check in file_checks:
            check.click()
        if not subfolder_checks and not file_checks:
            return
        
        del_button = self.driver.find_element(By.CSS_SELECTOR, 'input[value="Delete"]')
            
        if dry_run:
            log.info("dry_run, would delete %s/*", path)
            return
            
        del_button.click()

        result_text = self.driver.find_element(By.CSS_SELECTOR, "#description").text
        log.debug("result %s", result_text)
        if result_text != "The action was executed successfully":
            raise Exception(result_text)
    
    def ls_dirs(self, path:str):
        log.debug("ls %s", path)

        self.cd(path)

        subfolder_checks = self.driver.find_elements(By.NAME, "rm_folders[]")
        subfolder_rows = [check.find_element(By.XPATH, "../../..") for check in subfolder_checks]
        subfolder_names = [row.find_element(By.TAG_NAME, "a").text for row in subfolder_rows]

        return subfolder_names

    
    def upload_file(self, srcpath:str, dstdir:str) -> str:
        log.debug("upload %s -> %s", srcpath, dstdir)
        
        srcdir, srcname = os.path.split(srcpath)

        self.cd(dstdir)

        while True:
            form = self.driver.find_element(By.NAME, "uploadform")
            try:
                form.find_element(By.NAME, "FILE_UPLOAD[]").send_keys(os.path.abspath(srcpath))
            except StaleElementReferenceException:
                continue
            break
        form.find_element(By.CSS_SELECTOR, "#button").click()

        result_text = self.driver.find_element(By.CSS_SELECTOR, ".tdrow1").text
        log.debug("result %s", result_text)

        if "Files Uploaded" in result_text:
            pass # success
        elif "too large" in result_text:
            raise OSError(errno.EFBIG, result_text)
        elif "not an allowed file type" in result_text:
            raise PermissionError(result_text)
        else:
            raise Exception(result_text)
    
        # while True:
        #     table = self.driver.find_element(By.CSS_SELECTOR, "#acp_form .tableborder")
        #     try:
        #         labels = table.find_elements(By.LINK_TEXT, srcname)
        #     except NoSuchElementException as e:
        #         raise FileNotFoundError(srcpath) from e
        #     except StaleElementReferenceException:
        #         continue
        #     break
        # rows = [label.find_element(By.XPATH, "../..") for label in labels]
        # urls = [row.find_element(By.NAME, "copy").get_attribute("value") for row in rows]
        
        # if len(urls) != 1:
        #     raise FileExistsError(f"duplicated files: {urls}")
        # return urls[0]





    