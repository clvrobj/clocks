# -*- coding: utf-8 -*-
import sys
from tzlocal import get_localzone
from rumps import (debug_mode, App, clicked, MenuItem, timer,
                   separator, quit_application)
from clocks import Clocks

# intervals of the clocks change
DEFAULT_INTVL_STR = '3s'
INTVLS = ['3s', '5s', '10s', '30s', '1min']
INTVLS_MAP = {'3s': 3, '5s': 5, '10s': 10, '30s': 30, '1min': 60}

TIMEZONES = ['Asia/Dubai', 'Asia/Tokyo', 'Asia/Taipei',
             'Asia/Hong_Kong', 'Asia/Seoul', 'Asia/Bangkok',
             'America/New_York', 'America/Los_Angeles',
             'Europe/London', 'Europe/Stockholm', 'Europe/Amsterdam']


class ClockApp(App):

    def __init__(self):
        super(ClockApp, self).__init__("Clock", quit_button=None)
        self.init_menu()
        self.clocks = Clocks(times_to_flip=INTVLS_MAP.get(DEFAULT_INTVL_STR))
        self.add_local_clock()

    def init_menu(self):
        # add timezones menu
        self.timezones_menu = MenuItem('Time zones')
        for tz in TIMEZONES:
            self.timezones_menu.add(MenuItem(tz, callback=self.switch_clock_callback))
        # add interval menu
        self.interval_menu = MenuItem('Update time')
        for secs in INTVLS:
            item = MenuItem(secs, callback=self.update_interval)
            if secs == DEFAULT_INTVL_STR:
                item.state = 1
            self.interval_menu.add(item)
        self.quit_btn = MenuItem('Quit', callback=self.quit_app)
        self.menu = [self.timezones_menu, self.interval_menu, self.quit_btn]

    @timer(1)
    def update(self, _):
        self.title = self.clocks.get_clock_time_str()

    def update_interval(self, sender):
        for item in self.interval_menu.values():
            item.state = 0
        sender.state = 1
        self.clocks.set_times_to_flip(INTVLS_MAP.get(sender.title, 5))

    def add_clock(self, tz_name):
        if self.clocks.add_clock(tz_name):
            self.update_clocks_menu()

    def remove_clock(self, tz_name):
        if self.clocks.remove_clock(tz_name):
            self.update_clocks_menu()

    def update_clocks_menu(self):
        # reconstruct clocks menu
        items = []
        items.extend(self.clocks.get_all_clock_time_str())
        items.append(separator)
        items.append(self.timezones_menu)
        items.append(self.interval_menu)
        items.append(self.quit_btn)
        self.menu.clear()
        self.menu.update(items)

    def switch_clock_callback(self, sender):
        if sender.state == 0:
            self.add_clock(sender.title)
        else:
            self.remove_clock(sender.title)
        sender.state = not sender.state

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
        quit_application(sender)


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == 'debug':
        debug_mode(True)
    app = ClockApp()
    app.run()
