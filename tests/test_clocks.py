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
        clocks = Clocks()
        assert len(clocks.clocks) == 1
        tz_london = 'Europe/London'
        clocks.add_clock(tz_london)
        assert len(clocks.clocks) == 2
        assert clocks.clocks[1]['tz'].zone == tz_london
        tz_tokyo = 'Asia/Tokyo'
        clocks.add_clock(tz_tokyo)
        assert len(clocks.clocks) == 3
        assert clocks.clocks[2]['tz'].zone == tz_tokyo
        return

    def test_get_all_clock_time_str(self):
        clocks = Clocks()
        tz_london = 'Europe/London'
        tz_tokyo = 'Asia/Tokyo'
        clocks.add_clock(tz_london)
        clocks.add_clock(tz_tokyo)
        assert len(clocks.clocks) == 3
        clocks_strs = clocks.get_all_clock_time_str()
        assert len(clocks_strs) == 3


if __name__ == '__main__':
    unittest.main()
