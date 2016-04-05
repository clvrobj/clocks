# -*- coding: utf-8 -*-
from datetime import datetime
import rumps


class ClockApp(rumps.App):

    def __init__(self):
        super(ClockApp, self).__init__("Clock")
        self.menu = ["Preferences", "Silly button", "Say hi"]
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
        self.title = datetime.strftime(datetime.now(), '%H:%M')


if __name__ == "__main__":
    ClockApp().run()
