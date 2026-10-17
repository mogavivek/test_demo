"""
Main Flask application for the QA Automation Demo.

This application is intentionally simple.
The main purpose of this project is to demonstrate:

- Python web development
- UI automation with Playwright
- Pytest
- CI/CD with GitHub Actions
- Automated regression testing
"""
import os
import secrets

from dotenv import load_dotenv
from flask import Flask, jsonify, render_template, request

# Load environment variables from a local .env file if one exists.
load_dotenv()

def create_app():
    """
    Create and configure the Flask application.

    Returns:
        Flask: A configured Flask application instance.
    """
    
    # Create the Flask application.
    app = Flask(__name__)
    
    # Read the Flask secret key from an environment variable.
    #
    # IMPORTANT:
    # We never hard-code a real production secret in the source code.
    # For local development, a temporary random key is generated if
    # FLASK_SECRET_KEY is not provided.
    
    app.config["SECRET_KEY"] = os.getenv(
        "FLASK_SECRET_KEY",
        secrets.token_hex(32),
    )
    
    @app.route("/", methods=["GET"])
    def home():
        """
        Render the main QA Automation Demo webpage.

        Returns:
            HTML page containing the text input and submit button.
        """
        
        return render_template("index.html")
    
    @app.route("/submit", methods=["POST"])
    def submit_message():
        """
        Receive a message submitted from the frontend.

        The endpoint validates that the message is not empty and
        returns a JSON response that can be verified by Playwright.

        Returns:
            JSON response containing the submitted message and status.
        """
        
        # Read JSON data sent by the frontend.
        data = request.get_json(silent=True) or {}
        
        # Extract the message and remove unnecessary whitespace.
        message = str(data.get("message", "")).strip()
        
        # Validate that the user entered something.
        if not message:
            return jsonify(
                {
                    "success": False,
                    "message": "Message cannot be empty.",
                }
            ), 400
        
        # Return a successful response.
        return jsonify(
            {
                "success": True,
                "message": "Message received successfully!",
                "submitted_text": message,
            }
        )
    
    @app.route("/health", methods=["GET"])
    def health_check():
        """
        Provide a simple health-check endpoint.

        GitHub Actions uses this endpoint to confirm that the
        Flask application started successfully before running tests.

        Returns:
            JSON response indicating application health.
        """
        
        return jsonify(
            {
                "status": "healthy",
                "service": "QA Automation Demo",
            }
        )
    
    return app

# Create the Flask application instance.
app = create_app()

if __name__ == "__main__":
    # Start the Flask development server when this file is executed directly.
    app.run(
        host="127.0.0.1",
        port=5000,
        debug=False,
    )