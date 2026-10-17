"""
End-to-end UI tests for the QA Automation Demo.

The tests use:

- Pytest as the test framework
- Playwright as the browser automation framework
"""

from playwright.sync_api import Page, expect

BASE_URL = "http://127.0.0.1:5000"

def test_homepage_loads_successfully(page: Page):
    """
    Verify that the application homepage loads successfully.

    This test validates the most basic regression requirement:
    the website must be reachable and display the expected title.
    """
    
    # Open the application homepage.
    page.goto(BASE_URL)
    
    # Verify the browser title.
    expect(page).to_have_title("QA Automation Demo")
    
    # Verify that the main heading is visible.
    expect(
        page.get_by_role("heading", name="QA Automation Demo")
    ).to_be_visible()

def test_message_from_is_visible(page:Page):
    """
    Verify that all important form elements are available.

    The test checks the textarea and submit button that are
    required for the main user workflow.
    """

    # Open the application homepage.
    page.goto(BASE_URL)
    
    # Verify the message input exists.
    expect(
        page.locator("#message")
    ).to_be_visible()
    
    # Verify the submit button exists.
    expect(
        page.get_by_role("button", name="Submit")
    ).to_be_visible()

def test_user_can_submit_message(page:Page):
    """
    Verify the complete happy-path user workflow.

    Steps:
        1. Open the application.
        2. Enter a message.
        3. Click Submit.
        4. Verify the successful response.
    """

    # Open the application homepage.
    page.goto(BASE_URL)

    # Enter test data into the textarea.
    page.locator("#message").fill("Automated regression test")
    
    # Click the Submit button.
    page.get_by_role("button", name="Submit").click()
    
    # Verify the success response is displayed.
    expect(page.locator("#result")).to_be_visible()
    expect(page.locator("#result")).to_contain_text("Message received successfully!")
    
    # Verify that the submitted test data is displayed.
    expect(page.locator("#result")).to_be_visible()
    expect(page.locator("#result")).to_contain_text("Automated regression test")

def test_empty_message_validation(page:Page):
    """
    Verify that the application rejects empty input.

    This is a negative test case that protects the application's
    input validation behavior.
    """

    # Open the application homepage.
    page.goto(BASE_URL)

    # Click Submit without entering any message.
    page.get_by_role(
        "button",
        name="Submit"
    ).click()

    # Verify the expected validation message.
    expect(page.locator("#result")).to_be_visible()
    expect(page.locator("#result")).to_have_text("Please enter a message.")
    