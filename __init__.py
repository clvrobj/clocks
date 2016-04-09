# -*- coding: utf-8 -*-
from datetime import datetime
from dateutil.tz import tzlocal, tzoffset
from pytz import timezone
import rumps


class ClockApp(rumps.App):

    def __init__(self):
        super(ClockApp, self).__init__("Clock")
        self.menu = ["Preferences", "Silly button", "Say hi"]
        local = datetime.now(tzlocal()).tzname()
        self.clocks = [(local, None), ('LDN', timezone('Europe/London')),
                       ('TKO', timezone('Asia/Tokyo'))]
        self.counter_num = 0
        self.clock_idx = 0
        rumps.debug_mode(True)

    def get_display_title(self):
        if self.counter_num % 3 == 2:
            self.clock_idx += 1
            if self.clock_idx == len(self.clocks):
                self.clock_idx = 0
        clock = self.clocks[self.clock_idx]
        print self.counter_num, clock
        cur_time = datetime.now(clock[1]) if clock[1] else datetime.now()
        disp_time = datetime.strftime(cur_time, '%H:%M')
        title = '%s %s' % (clock[0], disp_time)
        self.counter_num += 1
        return title

    @rumps.clicked("Preferences")
    def prefs(self, _):
        rumps.alert(message='something', ok='YES!', cancel='NO!')

    @rumps.clicked("Silly button")
    def onoff(self, sender):
        sender.state = not sender.state

    @rumps.clicked("Say hi")
    def sayhi(self, _):
        rumps.notification("Awesome title", "amazing subtitle", "hi!!1")

    @rumps.timer(1)
    def update_time(self, _):
        self.title = self.get_display_title()


if __name__ == "__main__":
    ClockApp().run()
