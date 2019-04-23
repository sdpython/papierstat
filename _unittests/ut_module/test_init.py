"""
@brief      test log(time=0s)
"""
import unittest
from papierstat import check, _setup_hook


class TestInit(unittest.TestCase):

    def test_check(self):
        check()

    def test__setup_hook(self):
        _setup_hook()


if __name__ == "__main__":
    unittest.main()
