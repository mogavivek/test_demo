import os
from dotenv import load_dotenv
from playwright.sync_api import Page, expect
import pytest

load_dotenv()

BASE_URL = os.getenv("BASE_URL")

def test_dashboard_loads(page: Page):
    page.goto(BASE_URL)
    
    expect(page).to_have_title("Industrial Sensor Dashboard")
    expect(
        page.get_by_role("heading", name="Industrial Sensor Dashboard")
    ).to_be_visible()
    
@pytest.mark.skip
def test_user_can_add_sensor(page: Page):
    page.goto(BASE_URL)
    
    page.get_by_label("Sensor name").fill("UI-Pump-01")
    page.get_by_label("Temperature").fill("72.5")
    page.get_by_label("Status").select_option("online")
    
    page.get_by_role("button", name="Add sensor").click()
    
    expect(page.get_by_role("status")).to_have_text("Sensor added successfully")
    
    expect(page.get_by_role("list")).to_contain_text("UI-Pump-01: 72.5 °C (online)")
    
    
def test_duplicate_sensor_shows_error(page: Page):
    page.goto(BASE_URL)
    
    for _ in range(2):
        page.get_by_label("Sensor name").fill("UI-Duplica")
        page.get_by_label("Temperature").fill("58")
        page.get_by_role("button", name="Add sensor").click()
        
    expect(page.get_by_role("status")).to_contain_text("Sensor name already exists")
    