# -*- coding: utf-8 -*-
from datetime import datetime
from pytz import timezone
from tzlocal import get_localzone

TIMES_TO_FLIP = 10 # use next clock after being called FLIP_TIMES times

class Clocks(object):

    def __init__(self, tz_name='', times_to_flip=TIMES_TO_FLIP):
        self.clocks = []
        self.clock_idx = 0
        self.call_times = 0
        self.times_to_flip = times_to_flip
        # add the time zone input or the local zone by default
        tz_name = tz_name or get_localzone().zone
        self.add_clock(tz_name)

    def add_clock(self, tz_name):
        # TODO check the validation of tz name
        tz = timezone(tz_name)
        display_name = tz.zone.split('/')[-1].replace('_', ' ')
        self.clocks.append({'tz':tz, 'display_name':display_name})
        return

    def get_clock_time_str(self):
        if len(self.clocks) > 1:
            if self.call_times % self.times_to_flip == self.times_to_flip - 1:
                self.clock_idx += 1
                if self.clock_idx == len(self.clocks):
                    self.clock_idx = 0
        clock = self.clocks[self.clock_idx]
        cur_time = datetime.now(clock['tz'])
        disp_time = datetime.strftime(cur_time, '%H:%M')
        self.call_times += 1
        return '%s %s' % (clock['display_name'], disp_time)

    def set_times_to_flip(self, times_to_flip):
        self.times_to_flip = int(times_to_flip)
        self.call_times = 0

    def get_all_clock_display_name(self):
        ret = []
        for clock in self.clocks:
            ret.append(clock['display_name'])
        return ret

    def get_all_clock_time_str(self):
        ret = []
        for clock in self.clocks:
            cur_time = datetime.now(clock['tz'])
            disp_time = datetime.strftime(cur_time, '%H:%M')
            ret.append('%s %s' % (clock['display_name'], disp_time))
        return ret
