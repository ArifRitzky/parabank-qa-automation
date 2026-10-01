"""Runs the pytest suite and converts its JUnit XML into the JSON the dashboard displays."""
import subprocess
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parent
JUNIT_PATH = ROOT / "reports" / "junit.xml"


def parse_junit(xml_path):
    """Return one dict per test case: id, name, status (PASS/FAIL/ERROR/SKIPPED), duration, message, screenshot."""
    results = []
    for case in ET.parse(xml_path).getroot().iter("testcase"):
        props = {p.get("name"): p.get("value") for p in case.iter("property")}
        status, message = "PASS", ""

        failure = case.find("failure")
        error = case.find("error")
        skipped = case.find("skipped")
        if failure is not None:
            status, message = "FAIL", failure.get("message", "")
        elif error is not None:
            status, message = "ERROR", error.get("message", "")
        elif skipped is not None:
            status, message = "SKIPPED", skipped.get("message", "")

        results.append({
            "id": props.get("tc_id", case.get("name")),
            "name": case.get("name"),
            "status": status,
            "duration": round(float(case.get("time", 0)), 2),
            "message": message.strip().splitlines()[0] if message.strip() else "",
            "screenshot": props.get("screenshot"),
        })
    return results


def run_suite():
    JUNIT_PATH.parent.mkdir(exist_ok=True)
    if JUNIT_PATH.exists():
        JUNIT_PATH.unlink()
    subprocess.run(
        [sys.executable, "-m", "pytest", f"--junitxml={JUNIT_PATH}", "-q"],
        cwd=ROOT,
        check=False,
    )
    if not JUNIT_PATH.exists():
        raise RuntimeError("pytest produced no report (is Chrome/Selenium installed?)")
    return parse_junit(JUNIT_PATH)
