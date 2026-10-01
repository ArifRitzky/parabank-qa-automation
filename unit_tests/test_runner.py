"""Browser-free tests of the JUnit -> dashboard conversion. Run with: pytest unit_tests"""
import textwrap

from runner import parse_junit

SAMPLE = textwrap.dedent("""\
    <testsuites><testsuite name="pytest" tests="4">
      <testcase classname="tests.test_login" name="test_ok" time="1.234">
        <properties><property name="tc_id" value="TC-LOG-01"/></properties>
      </testcase>
      <testcase classname="tests.test_login" name="test_bad" time="2.5">
        <properties>
          <property name="tc_id" value="TC-LOG-02"/>
          <property name="screenshot" value="test_bad_1.png"/>
        </properties>
        <failure message="AssertionError: not shown&#10;details">trace</failure>
      </testcase>
      <testcase classname="tests.test_login" name="test_err" time="0.1">
        <error message="setup failed">trace</error>
      </testcase>
      <testcase classname="tests.test_login" name="test_skip" time="0">
        <skipped message="not today"/>
      </testcase>
    </testsuite></testsuites>
""")


def test_parse_junit_maps_every_status(tmp_path):
    path = tmp_path / "junit.xml"
    path.write_text(SAMPLE)

    ok, bad, err, skip = parse_junit(path)

    assert (ok["id"], ok["status"], ok["duration"]) == ("TC-LOG-01", "PASS", 1.23)
    assert (bad["status"], bad["screenshot"]) == ("FAIL", "test_bad_1.png")
    assert bad["message"] == "AssertionError: not shown"   # first line only
    assert (err["id"], err["status"]) == ("test_err", "ERROR")  # falls back to the test name
    assert skip["status"] == "SKIPPED"
