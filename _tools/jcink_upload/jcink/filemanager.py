import logging
log = logging.getLogger("fm")
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import InvalidSelectorException, NoSuchElementException, StaleElementReferenceException
import os
import errno
from .frame import frame_selected
from .adminpanel import AdminPanel


class FileManager:
    def __init__(self, ap: AdminPanel):
        self.driver = ap.driver
        self.ap = ap

    def cd_single(self, component:str):
        if component == "": # i.e. begin component was /
            log.info("nav to file manager page")
            self.ap.nav_to_section("File Manager")
        else:
            with frame_selected(self.driver, self.ap.body_frame):
                log.info("nav to %s", component)
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
        log.info("cd %s", path)
        components = path.split('/')
        for component in components:
            self.cd_single(component)
    
    def mkdir(self, path:str, parents=False):
        if parents:
            log.info("mkdir -p %s", path)
            self.mkdir_parents(path)
        elif path == "":
            pass
        else:
            log.info("mkdir %s", path)
            dirname, name = path.rsplit('/', 1)
            self.cd(dirname)

            log.info("create dir %s", name)
            # breakpoint()

            with frame_selected(self.driver, self.ap.body_frame):
                while True:
                    form = self.driver.find_element(By.NAME, "uploadform")
                    try:
                        form.find_element(By.NAME, "folder_name").send_keys(name)
                    except StaleElementReferenceException:
                        continue
                    break
                form.find_element(By.CSS_SELECTOR, "#button").click()

                result_text = self.driver.find_element(By.CSS_SELECTOR, ".tdrow1").text
            log.info("result %s", result_text)

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
    
    def rm(self, path:str, file=True, dir=True):
        log.info("rm %s", path)
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

        with frame_selected(self.driver, self.ap.body_frame):
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
            del_button.click()

            result_text = self.driver.find_element(By.CSS_SELECTOR, "#description").text
        log.info("result %s", result_text)
        if result_text != "The action was executed successfully":
            raise Exception(result_text)
    
    def upload_file(self, srcpath:str, dstdir:str) -> str:
        log.info("upload %s -> %s", srcpath, dstdir)
        
        srcdir, srcname = os.path.split(srcpath)

        self.cd(dstdir)
        with frame_selected(self.driver, self.ap.body_frame):
            while True:
                form = self.driver.find_element(By.NAME, "uploadform")
                try:
                    form.find_element(By.NAME, "FILE_UPLOAD[]").send_keys(os.path.abspath(srcpath))
                except StaleElementReferenceException:
                    continue
                break
            form.find_element(By.CSS_SELECTOR, "#button").click()

            result_text = self.driver.find_element(By.CSS_SELECTOR, ".tdrow1").text
            log.info("result %s", result_text)

            if "Files Uploaded" in result_text:
                pass # success
            elif "too large" in result_text:
                raise OSError(errno.EFBIG, result_text)
            elif "not an allowed file type" in result_text:
                raise PermissionError(result_text)
            else:
                raise Exception(result_text)
        
            # table = self.driver.find_element(By.CSS_SELECTOR, "#acp_form .tableborder")
            # try:
            #     labels = table.find_elements(By.LINK_TEXT, srcname) # <a> element
            # except NoSuchElementException as e:
            #     raise FileNotFoundError(srcpath) from e
            # except:
            #     breakpoint()
            # rows = [label.find_element(By.XPATH, "../..") for label in labels]
            # urls = [row.find_element(By.NAME, "copy").get_attribute("value") for row in rows]
            
            # if len(urls) != 1:
            #     raise FileExistsError(f"duplicated files: {urls}")
            # return urls[0]





    