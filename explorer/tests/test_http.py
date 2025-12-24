from explorer.http import get_csp_header_value


def test_get_csp_header_value():
    """Returns concatenated CSP directives for HTTP response header."""
    actual = get_csp_header_value('www.example.com')
    expected = "default-src 'self'; img-src 'self' www.example.com; media-src 'self' www.example.com; frame-src 'none'; frame-ancestors 'none'"

    assert actual == expected
