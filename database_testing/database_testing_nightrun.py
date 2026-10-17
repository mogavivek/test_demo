import logging
import pytest
import subprocess

from datetime import datetime
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
TEST_DIR = BASE_DIR / "tests"
REPORT_DIR = BASE_DIR / "reports"

REPORT_DIR.mkdir(parents=True, exist_ok=True)

timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

html_report = REPORT_DIR / f"report_{timestamp}.html"
allure_results = REPORT_DIR / f"allure_results_{timestamp}"
# Generated Allure HTML report
allure_html = REPORT_DIR / f"allure_report_{timestamp}"
xml_report = REPORT_DIR / f"report_{timestamp}.xml"
log_file = REPORT_DIR / f"report_{timestamp}.log"


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(log_file, encoding="utf-8"),
        logging.StreamHandler()
    ],
    force=True
)

logger = logging.getLogger(__name__)


def night_run():
    logger.info("Night run started")
    
    if not TEST_DIR.exists():
        logger.error("Tests directory not found: %s", TEST_DIR)
        return 2

    allure_results.mkdir(parents=True, exist_ok=True)
    
    pytest_args = [
        str(TEST_DIR),
        "-v",
        "--tb=short",

        # pytest HTML report
        f"--html={html_report}",
        "--self-contained-html",

        # JUnit XML report (optional)
        f"--junitxml={REPORT_DIR / f'junit_{timestamp}.xml'}",

        # Allure raw results
        f"--alluredir={allure_results}",

        # Log capture
        f"--log-file={log_file}",
        "--log-file-level=INFO",    
    ]
    
    try:
        exit_code = pytest.main(pytest_args)
        
        logger.info("Night run finished with exit code: %s", exit_code)
        
        # Build the Allure HTML report even if tests fail
        try:
            subprocess.run(
                [
                    "allure",
                    "generate",
                    str(allure_results),
                    "--clean",
                    "o",
                    str(allure_html),
                ],
                check=True,
                capture_output=True,
                text=True
            )
            logger.info("Allure HTML report generated: %s", allure_html)
        except FileNotFoundError:
            logger.exception(
                "Allure CLI not found. Install Allure and ensure it is "
                "available on PATH."
            )
            return 2
        
        except subprocess.CalledProcessError as e:
            logger.error("Allure report generation failed: %s", e.stderr)
            return 2
        
        logger.info("Pytest HTML report: %s", html_report)
        logger.info("Allure report: %s/index.html", allure_html)
        logger.info("Log file: %s", log_file)
        
        return int(exit_code)
    
    except Exception:
        logger.exception("Night run failed")
        return 2
    
    finally:
        logging.shutdown()
    

if __name__ == "__main__":
    raise SystemExit(night_run())