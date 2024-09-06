import logging
log = logging.getLogger("sm")
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import InvalidSelectorException, NoSuchElementException, StaleElementReferenceException
import os
import errno
import time
import re
from .adminpanel import AdminPanel


class SkinManager:
    def __init__(self, ap: AdminPanel):
        self.driver = ap.driver
        self.ap = ap

    def create_new(self, skinset_file):
        self.ap.nav_to_section("Manage Skin Sets")

        while True:
            form = self.driver.find_element(By.NAME, "uploadform")
            try:
                form.find_element(By.NAME, "FILE_UPLOAD").send_keys(os.path.abspath(skinset_file))
                form.find_element(By.CSS_SELECTOR, "#button").click()
            except StaleElementReferenceException:
                continue
            break

        while True:
            try:
                result_text = self.driver.find_element(By.CSS_SELECTOR, "#description").text
            except StaleElementReferenceException:
                continue
            break
        log.info("result %s", result_text)
        if result_text != "The action was executed successfully":
            raise Exception(result_text)
    
    def cleanup_skin_component(self, page_name:str, unallocated_table_name:str):
        self.ap.nav_to_section(page_name)
        while True:
            try:
                while True:
                    tables = self.driver.find_elements(By.CLASS_NAME, "tableborder")
                    table_candidates = tuple(t for t in tables if t.find_element(By.CLASS_NAME, "maintitle").text == unallocated_table_name)
                
                    if table_candidates:
                        table, = table_candidates
                    else:
                        break
                
                    table.find_element(By.LINK_TEXT, "Remove").click()
                    # time.sleep(0.1)
                    self.driver.switch_to.alert.accept()
                    time.sleep(0.5)

            except StaleElementReferenceException:
                continue
            break

    def cleanup_wrappers(self):
        return self.cleanup_skin_component("Board Wrappers", "Current Unallocated Wrappers")
    def cleanup_stylesheets(self):
        return self.cleanup_skin_component("Style Sheets", "Current Unallocated Stylesheets")
    def cleanup_macros(self):
        return self.cleanup_skin_component("Macros", "Current Unallocated Macro sets")
    def cleanup_templates(self):
        return self.cleanup_skin_component("HTML Templates", "Unallocated HTML Template sets")
    def cleanup_unused_skins(self):
        return self.cleanup_skin_component("Manage Skin Sets", "Skin Sets not used by Members")
    
    def cleanup(self):
        self.cleanup_wrappers()
        self.cleanup_stylesheets()
        self.cleanup_macros()
        self.cleanup_templates()
    
    
    def list_skins(self, pattern:str|re.Pattern) -> list[re.Match]:
        pattern = re.compile(pattern)
        self.ap.nav_to_section("Manage Skin Sets")
        
        while True:
            tables = self.driver.find_elements(By.CLASS_NAME, "tableborder")
            try:
                used_table_candidates = tuple(t for t in tables if t.find_element(By.CLASS_NAME, "maintitle").text == "Current Skins Used by Members")
                if used_table_candidates:
                    table, = used_table_candidates
                    used_list = list(self.extract_skin_names_from_table(pattern, table))
                else:
                    used_list = []
            
                notused_table_candidates = tuple(t for t in tables if t.find_element(By.CLASS_NAME, "maintitle").text == "Skin Sets not used by Members")
                if notused_table_candidates:
                    table, = notused_table_candidates
                    notused_list = list(self.extract_skin_names_from_table(pattern, table))
                else:
                    notused_list = []
            except StaleElementReferenceException:
                continue
            break

        return used_list + notused_list
    
    def extract_skin_names_from_table(self, pattern:re.Pattern, table:WebElement):
        maybe_skin_name_cells = table.find_elements(By.CSS_SELECTOR, 'td.tdrow1 b')
        for cell in maybe_skin_name_cells:
            maybe_skin_name = cell.text
            m = pattern.match(maybe_skin_name)
            if m:
                log.info("discovered skin: %s", m.group(0))
                yield m

    def upgrade_skin(self, orig:str, new:str, dry_run=False):
        self.ap.nav_to_section("Manage Skin Sets")

        while True:
            try:
                self.driver.find_element(By.NAME, "oid").send_keys(orig)
                self.driver.find_element(By.NAME, "nid").send_keys(new)
                if dry_run:
                    log.info("dry_run: would have upgraded from '%s' to '%s'", orig, new)
                    return
                self.driver.find_element(By.CSS_SELECTOR, '[value="Update members skin choice"]').click()
            except StaleElementReferenceException:
                continue
            break

        while True:
            try:
                result_text = self.driver.find_element(By.CSS_SELECTOR, "#description").text
            except StaleElementReferenceException:
                continue
            break
        log.info("result %s", result_text)
        if result_text != "The action was executed successfully":
            raise Exception(result_text)
        
    def delete_skin(self, skin:str, dry_run=False):
        self.ap.nav_to_section("Manage Skin Sets")

        while True:
            try:
                tables = self.driver.find_elements(By.CLASS_NAME, "tableborder")
                table_candidates = tuple(t for t in tables if t.find_element(By.CLASS_NAME, "maintitle").text == "Skin Sets not used by Members")
                table, = table_candidates
                name_cell_candidates = tuple(c for c in table.find_elements(By.CSS_SELECTOR, 'td.tdrow1 b') if c.text==skin)
                name_cell, = name_cell_candidates
                row = name_cell.find_element(By.XPATH, "../..")
                remove_link = row.find_element(By.LINK_TEXT, "Remove")

                if dry_run:
                    log.info("dry_run: would remove %s", skin)
                    return
                
                remove_link.click()
                # time.sleep(0.1)
                self.driver.switch_to.alert.accept()
                time.sleep(0.5)

            except StaleElementReferenceException:
                continue
            break