# -*- coding: utf-8 -*-
from datetime import datetime
from pytz import timezone

TIMES_TO_FLIP = 10 # use next clock after being called FLIP_TIMES times

class Clocks(object):

    def __init__(self, tz_name='', times_to_flip=TIMES_TO_FLIP):
        self.clocks = {} # {tz_name:{tz_name, display_name}, ...} # TODO creat a class
        self.clock_keys = [] # tz names
        self.clock_idx = 0 # TODO start from 0 or -1
        self.call_times = 0
        self.times_to_flip = times_to_flip
        if tz_name:
            tz_name = tz_name
            self.add_clock(tz_name)

    def get_clock_by_idx(self, idx):
        return self.clocks[self.clock_keys[idx]]

    def add_clock(self, tz_name):
        # TODO check the validation of tz name
        if tz_name in self.clock_keys:
            return False
        tz = timezone(tz_name)
        display_name = tz.zone.split('/')[-1].replace('_', ' ')
        self.clock_keys.append(tz_name)
        self.clocks[tz_name] = {'tz':tz, 'display_name':display_name}
        return True

    def remove_clock(self, tz_name):
        if tz_name not in self.clock_keys:
            return False
        self.clock_keys.remove(tz_name)
        self.clock_idx = 0
        return True

    def get_clock_time_str(self):
        if len(self.clock_keys) == 0:
            return
        if len(self.clock_keys) > 1:
            if self.call_times % self.times_to_flip == self.times_to_flip - 1:
                self.clock_idx += 1
                if self.clock_idx == len(self.clock_keys):
                    self.clock_idx = 0
        clock = self.clocks[self.clock_keys[self.clock_idx]]
        cur_time = datetime.now(clock['tz'])
        disp_time = datetime.strftime(cur_time, '%H:%M')
        self.call_times += 1
        return '%s %s' % (clock['display_name'], disp_time)

    def set_times_to_flip(self, times_to_flip):
        self.times_to_flip = int(times_to_flip)
        self.call_times = 0

    def get_all_clock_display_name(self):
        ret = []
        for tz_name in self.clock_keys:
            clock = self.clocks[tz_name]
            ret.append(clock['display_name'])
        return ret

    def get_all_clock_time_str(self):
        ret = []
        for tz_name in self.clock_keys:
            clock = self.clocks[tz_name]
            cur_time = datetime.now(clock['tz'])
            disp_time = datetime.strftime(cur_time, '%H:%M')
            ret.append('%s %s' % (clock['display_name'], disp_time))
        return ret
