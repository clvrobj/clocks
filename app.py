# -*- coding: utf-8 -*-
import rumps
from clocks import Clocks


class ClockApp(rumps.App):

    def __init__(self):
        super(ClockApp, self).__init__("Clock")
        self.menu = ["Preferences", "Silly button", "Say hi"]
        self.clocks = Clocks()
        self.clocks.add_clock('Europe/London')
        self.clocks.add_clock('Asia/Tokyo')
        rumps.debug_mode(True)

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
        self.title = self.clocks.get_clock_time_str()


if __name__ == "__main__":
    ClockApp().run()
