import pytest
import logging
import csv
from pathlib import Path

# project root = parent of tests folder
BASE_DIR = Path(__file__).resolve().parent.parent
REPORT_DIR = BASE_DIR / "reports"
REPORT_DIR.mkdir(exist_ok=True)
    
    
import logging

def pytest_configure(config):
    log_file = REPORT_DIR / "test.log"

    logging.basicConfig(
        filename=log_file,
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s"
    )

# dictionary to store test results
test_results = {}

@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item, call):
    # Execute all other hooks to get the report object
    outcome = yield
    rep = outcome.get_result()
    
    # Only store after the call phase (when the test actually runs)
    if rep.when == "call":
        # item.nodeid is the test name
        test_results[item.nodeid] = rep.outcome

# -------------------------
# AFTER ALL TESTS FINISH
# -------------------------
def pytest_sessionfinish(session, exitstatus):

    file_path = REPORT_DIR / "test_results.csv"

    with open(file_path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Test", "Result"])

        for test, result in test_results.items():
            writer.writerow([test, result])