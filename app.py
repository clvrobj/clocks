# -*- coding: utf-8 -*-
import os
import sys
import pytz
import pickle
from tzlocal import get_localzone
from rumps import (debug_mode, App, clicked, MenuItem, timer,
                   separator, application_support, quit_application)
from clocks import Clocks

APP_NAME = 'Clocks'
SUPPORT_CLOCKS_FILENAME = 'clocks_tz'
SUPPORT_INTVL_FILENAME = 'intvl'

# intervals of the clocks change
DEFAULT_INTVL_STR = '3s'
INTVLS = ['3s', '5s', '10s', '30s', '1min']
INTVLS_MAP = {'3s': 3, '5s': 5, '10s': 10, '30s': 30, '1min': 60}

TIMEZONES = pytz.common_timezones

class ClockApp(App):

    def __init__(self):
        super(ClockApp, self).__init__("Clock", quit_button=None)
        self.init_menu()
        self.clocks = Clocks(times_to_flip=INTVLS_MAP.get(DEFAULT_INTVL_STR))
        self.load_clocks_data()
        self.load_intvl_data()

    def load_clocks_data(self):
        clocks_tz = []
        filepath = application_support(APP_NAME) + '/' + SUPPORT_CLOCKS_FILENAME
        if os.path.exists(filepath):
            f = open(filepath, 'r')
            for e in pickle.load(f):
                if isinstance(e, str):
                    clocks_tz.append(e)
        if len(clocks_tz) > 0:
            for tz in clocks_tz:
                self.add_clock(tz)
        else:
            self.add_local_clock()
        return

    def dump_clocks_data(self):
        filepath = application_support(APP_NAME) + '/' + SUPPORT_CLOCKS_FILENAME
        f = open(filepath, 'wb')
        pickle.dump(self.clocks.clock_keys, f)
        return

    def load_intvl_data(self):
        filepath = application_support(APP_NAME) + '/' + SUPPORT_INTVL_FILENAME
        if os.path.exists(filepath):
            f = open(filepath, 'r')
            intvl = pickle.load(f)
            self.clocks.set_times_to_flip(intvl)
            for s, i in INTVLS_MAP.items():
                self.interval_menu[s].state = 1 if i == intvl else 0

    def dump_intvl_data(self):
        filepath = application_support(APP_NAME) + '/' + SUPPORT_INTVL_FILENAME
        f = open(filepath, 'wb')
        pickle.dump(self.clocks.times_to_flip, f)
        return

    def init_menu(self):
        # add timezones menu
        self.timezones_menu = MenuItem('Time Zones')
        for tz in TIMEZONES:
            self.timezones_menu.add(MenuItem(tz, callback=self.switch_clock_callback))
        # recently added menu
        self.recent_menu = MenuItem('Add Recent')
        # add interval menu
        self.interval_menu = MenuItem('Update Time')
        for secs in INTVLS:
            item = MenuItem(secs, callback=self.update_interval)
            if secs == DEFAULT_INTVL_STR:
                item.state = 1
            self.interval_menu.add(item)
        self.quit_btn = MenuItem('Quit', callback=self.quit_app)
        self.menu = [self.timezones_menu, self.recent_menu,
                     self.interval_menu, self.quit_btn]

    @timer(1)
    def update(self, _):
        self.title = self.clocks.get_clock_time_str()
        self.update_clocks_menu()

    def update_interval(self, sender):
        for item in self.interval_menu.values():
            item.state = 0
        sender.state = 1
        self.clocks.set_times_to_flip(INTVLS_MAP.get(sender.title, 5))

    def add_clock(self, tz_name):
        if self.clocks.add_clock(tz_name):
            self.update_clocks_menu()
            self.timezones_menu[tz_name].state = 1

    def remove_clock(self, tz_name):
        if self.clocks.remove_clock(tz_name):
            self.update_clocks_menu()
            self.timezones_menu[tz_name].state = 0

    def update_clocks_menu(self):
        # reconstruct clocks menu
        items = []
        items.extend(self.clocks.get_all_clock_time_str())
        items.append(separator)
        items.append(self.timezones_menu)
        if len(self.recent_menu.keys()) > 0:
            self.recent_menu.clear()
        for c in self.clocks.get_history_clocks():
            self.recent_menu.add(
                MenuItem(c, callback=self.add_clock_from_recent_callback))
        items.append(self.recent_menu)
        items.append(self.interval_menu)
        items.append(self.quit_btn)
        self.menu.clear()
        self.menu.update(items)

    def switch_clock_callback(self, sender):
        tz_name = str(sender.title)
        if sender.state == 0:
            self.add_clock(tz_name)
        else:
            self.remove_clock(tz_name)

    def add_clock_from_recent_callback(self, sender):
        tz_name = str(sender.title)
        self.add_clock(tz_name)
        self.timezones_menu[tz_name].state = 1

    def add_local_clock(self):
        # add local zone by default
        local_zone = get_localzone().zone
        self.add_clock(local_zone)
        if self.timezones_menu.has_key(local_zone):
            self.timezones_menu[local_zone].state = 1
        else:
            item = MenuItem(local_zone, callback=self.switch_clock_callback)
            item.state = 1
            self.timezones_menu.add(item)

    def quit_app(self, sender):
        self.dump_clocks_data()
        self.dump_intvl_data()
        quit_application(sender)


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == 'debug':
        debug_mode(True)
    app = ClockApp()
    app.run()
