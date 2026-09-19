# QA Automation Framework - Core Banking Simulation

An automated End-to-End (E2E) testing framework designed for core banking customer modules (Registration & Login). Built with Python and Selenium, and integrated with a custom FastAPI backend to render real-time execution metrics on a web dashboard.

## Key Features

- **Modular Test Architecture:** Test scenarios are isolated using the Page Object Model (POM) concept for maintainability.
- **Dynamic Data Passing:** Seamlessly passes variables (e.g., generated Usernames and Passwords) between test scripts (Registration -> Login).
- **Session Isolation:** Implements strict browser session management (`delete_all_cookies`) to ensure independent test states without reopening the browser instance.
- **Automated Bug Evidence:** Automatically captures and routes screenshots to a dedicated directory upon test failure (`FAIL`) or execution error (`ERROR`).
- **Real-Time Web Dashboard:** A frontend interface that communicates with the testing server via REST API to visualize execution status, execution time, and error logs dynamically.

## Technology Stack

- **Testing Engine:** Python 3, Selenium WebDriver
- **Backend API:** FastAPI, Uvicorn
- **Frontend Dashboard:** HTML5, CSS3, Vanilla JavaScript

## Project Structure

```text
QA_Project/
├── frontend/               # UI Dashboard (HTML, CSS, JS)
├── tests/                  # Selenium automation test scripts
│   ├── test_parabank_reg.py
│   ├── test_parabank_login.py
├── screenshots/            # Auto-generated evidence for failed tests
├── main.py                 # FastAPI server & test runner manager
└── README.md
```
