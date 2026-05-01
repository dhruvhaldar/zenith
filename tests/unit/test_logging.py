import logging
import io
from api.index import SanitizedFormatter

def test_sanitized_formatter_terminal_escapes():
    logger = logging.getLogger('test_logger')
    logger.setLevel(logging.DEBUG)
    log_capture = io.StringIO()
    handler = logging.StreamHandler(log_capture)
    handler.setFormatter(SanitizedFormatter('%(message)s'))
    logger.addHandler(handler)

    logger.warning("Normal text \x1B[31mHACKED\x1B[0m text \x08\x08 and \x00 null \t tab \n newline \r")

    log_contents = log_capture.getvalue()

    assert "HACKED" in log_contents
    assert "\x1B" not in log_contents
    assert "\x08" not in log_contents
    assert "\x00" not in log_contents
    assert "tab" in log_contents
    assert "\n" in log_contents # Handler adds a final newline, but our internal \n is replaced
    assert "newline" in log_contents

    logger.removeHandler(handler)
