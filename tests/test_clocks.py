# -*- coding:utf-8 -*-
import os
import sys
APP_DIR = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.insert(0, APP_DIR)

import unittest
from clocks import Clocks

class ClocksTest(unittest.TestCase):

    def test_init_clock(self):
        from tzlocal import get_localzone
        local_tz_name = get_localzone().zone
        clocks = Clocks()
        assert len(clocks.clocks) == 1
        assert local_tz_name == clocks.clocks[0]['tz'].zone
        return

    def test_add_clock(self):
        assert 1 == 1
        return


if __name__ == '__main__':
    unittest.main()
