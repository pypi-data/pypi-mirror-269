import sys
import os.path
import io
import unittest
from unittest.mock import patch

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from cmgr import command_line  # noqa: linter (pycodestyle) should not lint this line.


class test_cmgr(unittest.TestCase):
    """command-line cmgr unittest"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_version(self):
        with patch("sys.stdout", new=io.StringIO()) as fake_out:
            self.assertRaises(SystemExit, command_line.main, ['--version'])
            self.assertIn('.', fake_out.getvalue())


if __name__ == "__main__":
    unittest.main(verbosity=2, exit=False)
