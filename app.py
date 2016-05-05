# -*- coding: utf-8 -*-
from rumps import App, clicked, MenuItem, timer, debug_mode
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
        self.clocks.add_clock('Europe/London')
        self.clocks.add_clock('Europe/Amsterdam')
        # self.clocks.add_clock('Asia/Tokyo')
        debug_mode(True)

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


if __name__ == "__main__":
    app = ClockApp()
    app.run()

