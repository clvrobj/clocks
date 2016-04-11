# -*- coding: utf-8 -*-
from datetime import datetime
from pytz import timezone
from tzlocal import get_localzone

FLIP_TIMES = 6 # use next clock after being called FLIP_TIMES times

class Clocks(object):

    def __init__(self):
        local_zone = get_localzone()
        local_zone_name = local_zone.zone.split('/')[-1]
        self.clocks = [(local_zone_name, local_zone)]
        self.clock_idx = 0
        self.call_times = 0

    def add_clock(self, tz_name):
        tz = timezone(tz_name)
        tz_name = tz.zone.split('/')[-1]
        self.clocks.append((tz_name, tz))
        return

    def get_clock_time_str(self):
        if self.call_times % FLIP_TIMES == FLIP_TIMES - 1:
            self.clock_idx += 1
            if self.clock_idx == len(self.clocks):
                self.clock_idx = 0
        clock = self.clocks[self.clock_idx]
        cur_time = datetime.now(clock[1]) if clock[1] else datetime.now()
        disp_time = datetime.strftime(cur_time, '%H:%M')
        self.call_times += 1
        return '%s %s' % (clock[0], disp_time)
