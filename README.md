# QA Automation Framework: ParaBank (Registration & Login)

End-to-end UI test suite built with **Python, Selenium and pytest**, using the **Page Object Model**. It tests the **public ParaBank demo app** (https://parabank.parasoft.com), which Parasoft provides for test-automation practice. It is not a real banking system.

A small FastAPI app runs the suite and serves a web dashboard with per-test status, duration and failure screenshots.

## What is tested

| ID | Scenario | Type |
|---|---|---|
| TC-REG-01 | Register with valid data | Positive |
| TC-REG-02 | Submit empty form shows all mandatory-field errors | Negative |
| TC-REG-03 | Mismatched password confirmation is rejected | Negative |
| TC-REG-04 | Re-using an existing username is rejected | Negative |
| TC-LOG-01 | Login with valid credentials shows Accounts Overview | Positive |
| TC-LOG-02 | Wrong password is rejected | Negative |
| TC-LOG-03 | Unknown username is rejected | Negative |
| TC-LOG-04 | Empty credentials are rejected | Negative |

## Design

- **Page Object Model**: locators and page actions live in `pages/`; tests in `tests/` contain only scenario steps and assertions.
- **Explicit waits** (`WebDriverWait`), no fixed `sleep()` calls.
- **Independent tests**: each test gets a fresh browser. Login tests use a session fixture that registers one account up front, so they do not depend on the registration tests.
- **Failure evidence**: a screenshot is saved to `screenshots/` for every failed test and linked from the dashboard.
- **Unique test data**: usernames are uuid-based to avoid collisions on the shared demo server.

## Project structure

```text
pages/            Page objects (BasePage, RegisterPage, LoginPage, AccountsOverviewPage) + test data
tests/            pytest E2E tests and conftest.py (browser fixture, screenshot-on-failure hook)
unit_tests/       Browser-free tests of the report conversion (runner.py)
runner.py         Runs pytest, converts JUnit XML to dashboard JSON
main.py           FastAPI app: POST /run-test, serves the dashboard
frontend/         Dashboard (HTML, CSS, vanilla JS)
```

## Setup

Requires Python 3.10+ and Google Chrome (Selenium 4 downloads the matching driver automatically).

```bash
python -m venv .venv
.venv\Scripts\activate          # Windows;  source .venv/bin/activate on macOS/Linux
pip install -r requirements.txt
```

## Run

Tests directly:

```bash
pytest                          # visible browser
HEADLESS=1 pytest               # headless (Windows cmd: set HEADLESS=1)
pytest -m "tc_id" -k login      # only the login tests
pytest unit_tests               # fast, no browser
```

Dashboard:

```bash
uvicorn main:app
# open http://127.0.0.1:8000 and click "Run All Scenarios"
```

The server only binds to localhost by default. Do not expose it publicly: the endpoint launches a browser on the host.

## Known limitations

- ParaBank is a shared public demo that is sometimes slow or reset. A failed run does not always mean a defect in the tests; re-run before investigating.
- Only registration and login are covered. Account overview, transfers and bill pay are not yet automated.
- No CI pipeline yet; running against a public demo site from CI would be flaky.
- Tests run sequentially, one browser at a time.
