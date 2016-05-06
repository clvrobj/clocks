# -*- coding: utf-8 -*-
import sys
from rumps import debug_mode, App, clicked, MenuItem, timer, separator
from clocks import Clocks

# intervals of the clocks change
DEFAULT_INTVL_STR = '10s'
INTVLS = ['5s', '10s', '30s', '1min']
INTVLS_MAP = {'5s': 5, '10s': 10, '30s': 30, '1min': 60}

class ClockApp(App):

    def __init__(self):
        super(ClockApp, self).__init__("Clock")
        self.init_menu()
        self.clocks = Clocks(times_to_flip=INTVLS_MAP.get(DEFAULT_INTVL_STR))
        self.add_clock('Europe/London')
        self.add_clock('Europe/Amsterdam')
        # self.add_clock('Asia/Tokyo')

    def init_menu(self):
        self.interval_menu = MenuItem('Update time')
        for secs in INTVLS:
            item = MenuItem(secs, callback=self.update_interval)
            if secs == DEFAULT_INTVL_STR:
                item.state = 1
            self.interval_menu.add(item)
        self.menu = [self.interval_menu]

    @timer(1)
    def update(self, _):
        self.title = self.clocks.get_clock_time_str()

    def update_interval(self, sender):
        for item in self.interval_menu.values():
            item.state = 0
        sender.state = 1
        self.clocks.set_times_to_flip(INTVLS_MAP.get(sender.title, 5))

    def add_clock(self, tz_name):
        self.clocks.add_clock(tz_name)
        # reconstruct clocks menu
        items = []
        items.extend(self.clocks.get_all_clock_time_str())
        items.append(separator)
        items.append(self.interval_menu)
        self.menu.clear()
        self.menu.update(items)


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == 'debug':
        debug_mode(True)
    app = ClockApp()
    app.run()
