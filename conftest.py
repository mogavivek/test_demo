import pytest
from selenium import webdriver

@pytest.fixture(scope="class")
def browser():
    driver = webdriver.Chrome()
    driver.maximize_window()
    yield driver
    driver.quit()