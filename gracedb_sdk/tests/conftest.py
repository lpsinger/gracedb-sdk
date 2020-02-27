from requests.exceptions import HTTPError


def pytest_runtest_makereport(item, call):
    """Capture HTTP response content for pytest reports."""
    if call.excinfo is not None and call.excinfo.errisinstance(HTTPError):
        item.add_report_section(
            'call', 'HTTP response content', call.excinfo.value.response.text)
