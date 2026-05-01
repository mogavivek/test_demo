import mos_customer_frontends_interaction.utilities.common.project_global_constants as cons

import sys
path_to_packages = '\\Utilities\\lib_ecutest\\'
sys.path.append(path_to_packages + 'selenium-4.0.0-py3-none-any\\')
sys.path.append(path_to_packages + 'certifi-2021.10.8-py2.py3-none-any\\')
sys.path.append(path_to_packages + 'urllib3-1.26.7-py2.py3-none-any\\')
sys.path.append(path_to_packages + 'PyAutoGUI-0.9.53\\')
sys.path.append(path_to_packages + 'pyperclip-1.8.2\\')

from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
import pyautogui
import time
from datetime import datetime
import inspect


class SeleniumInteraction:
    def __init__(self, path_to_test_report):
        """
        This class creates an interaction layer with websites via selenium commands

        Arguments:
            platform_name : the platform of the phone, e. g. Android or iOS
            path_to_test_report : the path to the test report of an ECU-Test test case using this class to interact with phones
        """
        self.path_to_test_report = path_to_test_report

    def start_driver(self):
        """
        This function creates a selenium webdriver instance either for firefox
        """
        self.service_log_path= self.path_to_test_report + "geckodriver.log"
        self.options = Options()
        self.driver = webdriver.Firefox(
            executable_path = cons.PATH_TO_GECKODRIVER, 
            service_log_path = self.service_log_path, 
            options=self.options)
        
    def stop_driver(self):
        """
        This function quits the driver instance and takes a final screenshot
        """
        self.take_screenshot()
        self.driver.quit()

    def find_element_by_xpath(self, xpath, timeout):
        """
        This function tries to find an element by using the find by xpath method from selenium

        Arguments:
            xpath : the xpath that should be found
            timeout: how long you want to wait until the search process is aborted
        Return: the element if found. Otherwise none is returned
        """
        #print("Used xpath: " + str(xpath))
        return wait(self.driver, timeout).until(EC.visibility_of_element_located((By.XPATH, xpath)))

    def find_element_by_id(self, id_of_element, timeout):
        """
        This function tries to find an element by using the find by id method from selenium

        Arguments:
            id_of_element : the ID that should be found
            timeout: how long you want to wait until the search process is aborted
        Return: the element if found. Otherwise none is returned
        """
        return wait(self.driver, timeout).until(EC.visibility_of_element_located((By.ID, id_of_element)))

    def find_element_by_tag_name(self, element, tag_of_element):
        """
        This function tries to find an element by using the find by tag name method from selenium

        Arguments:
            tag_of_element : the tag name that should be found
            element: name of element in which to look for the specivied tag_of_element
        Return: the element if found. Otherwise none is returned
        """
        return element.find_elements(By.TAG_NAME, tag_of_element)

    def execute_script(self, script_name, object_name):
        """
        This function executes various scripts

        Arguments:
            script_name : name of script to be executed e.g. "arguments[0].click();"
            object_name: object on which the script will be executed
        Return: no return
        """
        return self.driver.execute_script(script_name, object_name)

    def wait_for_website_to_load(self, timeout):
        """
        This function waits until the driver is done loading the website

        Arguments:
            timeout: how long you want to wait until the waiting process is aborted
        """
        wait(self.driver, timeout).until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
    
    def open_new_driver_tab(self, link):
        """
        This function opens a website in a new tab

        Arguments:
            link: the URL of the website for the new tab
        Return: the element if found. Otherwise none is returned
        """
        self.driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.COMMAND + 't')
        self.driver.get(link)

    def browser_switch_to_another_tab(self, tab_number, wait_time):
        """
        This function switches to another preexisting tab of the browser

        Arguments:
            tab_number: the number of the tab you want to switch to
            wait_time: the wait time after switching to the tab before returning
        Return: the URL of the tab that was switched to
        """
        handles = self.driver.window_handles
        self.driver.switch_to.window(handles[tab_number])
        time.sleep(wait_time)
        return self.driver.current_url

    def copy_and_paste_string(self, req_string):
        """
        This function executes the copy and paste command for a string

        Arguments:
            req_string: the string you want to paste
        """
        for character in list(req_string):
            pyperclip.copy(character)
            pyautogui.hotkey('ctrl', 'v')
            time.sleep(0.5)

    def take_screenshot(self):
        """
        This functions takes a screenshot of the website and saves it to the test report folder
        """
        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        dt_string = dt_string.replace('/', '_')
        dt_string = dt_string.replace(' ', '_')
        dt_string = dt_string.replace(':', '_')
        path = self.path_to_test_report + '\\' + inspect.stack()[2][3] + dt_string + '.png'
        self.driver.save_screenshot(path)

    def scroll_down(self):
        """
        This function scrolls down on a website
        """
        html = self.driver.find_element(By.TAG_NAME, 'html')
        html.send_keys(Keys.PAGE_DOWN)
        time.sleep(1)

        
    def scroll_up(self):
        """
        This function scrolls up on a website
        """
        html = self.driver.find_element(By.TAG_NAME, 'html')
        html.send_keys(Keys.PAGE_UP)
        time.sleep(1)

    def find_element_by_xpath_and_save_as_image(self, xpath, file_path):
        wait(self.driver, 3).until(EC.visibility_of_element_located((By.XPATH, xpath))).screenshot(file_path)