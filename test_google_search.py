import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

search_keywords = ['Selenium Python', 'Python Selenium', 'Search selenium']

class TestGoogleSearch:

    @pytest.mark.parametrize("search_keyword", search_keywords)
    def test_search(self, browser, search_keyword):
        driver = browser
        driver.get("https://www.google.com/")

        search_box = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "input"))
        )

        search_box.send_keys(search_keyword)
        search_box.send_keys(Keys.RETURN)
        time.sleep(2)

        assert search_keyword in driver.title