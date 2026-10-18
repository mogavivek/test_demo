import pytest
from fastapi.testclient import TestClient

import main_app as application

@pytest.fixture
def client(tmp_path, monkeypatch):
    # Give each test an independent temporary database.
    test_db = tmp_path / "test_sensor.db"
    
    monkeypatch.setattr(application, "DB_PATH", test_db)
    application.init_db()
    
    with TestClient(application.app) as test_client:
        yield test_client

import pytest
from playwright.sync_api import sync_playwright
from pathlib import Path
import logging

# First it goes to the base directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Then it creates the directories if not exsists but if it is exsists then it will not create the directories
VIDEO_DIR = BASE_DIR / "videos"
SCREENSHOT_DIR = BASE_DIR / "screenshots"
TRACE_DIR = BASE_DIR / "traces"
REPORT_DIR = BASE_DIR / "reports"

REPORT_DIR.mkdir(exist_ok=True)
VIDEO_DIR.mkdir(exist_ok=True)
SCREENSHOT_DIR.mkdir(exist_ok=True)
TRACE_DIR.mkdir(exist_ok=True)
LOG_DIR = BASE_DIR / "logs"
LOG_DIR.mkdir(exist_ok=True)

LOG_FILE = LOG_DIR / "execution.log"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE), logging.StreamHandler()]
    )

logger = logging.getLogger(__name__)

# scope "session" type means it will runs once at begining of the test runs
@pytest.fixture(scope="session")
def set_up_tear_down():
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=False, # To see the pages
            slow_mo=100,
            args=["--start-maximized"]
        )
        yield browser
        browser.close() # Tear down condition

# This will open the browser window in given dimension of the window
# Then it will store the screenshots, videos and traces
@pytest.fixture(scope="session")
def browser_context(set_up_tear_down, request):
    context = set_up_tear_down.new_context(
        # viewport={"width":1920, "height":1080}, # This use if need a specific size of the window
        no_viewport=True,
        record_video_dir=str(VIDEO_DIR)
    )
    context.tracing.start(
        screenshots=True,
        snapshots=True,
        sources=True
    )  
    yield context

    context.tracing.stop(
        path=str(TRACE_DIR / f"{request.node.name}.zip"))
    context.close()


@pytest.fixture(scope="session")
def page(browser_context, request):
    page = browser_context.new_page()
    page.set_default_timeout(20000)
    page.set_default_navigation_timeout(30000)
    yield page
    page.screenshot(path=str(SCREENSHOT_DIR / f"{request.node.name}.png"))