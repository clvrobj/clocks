# -*- coding: utf-8 -*-
from rumps import App, clicked, MenuItem, timer
from clocks import Clocks


class ClockApp(App):

    def __init__(self):
        super(ClockApp, self).__init__("Clock")
        self.menu = ["Preferences", "Silly button", "Say hi"]
        self.clocks = Clocks(flip_times=8)
        self.clocks.add_clock('Europe/London')
        self.clocks.add_clock('Europe/Amsterdam')
        # self.clocks.add_clock('Asia/Tokyo')
        # rumps.debug_mode(True)

    # @rumps.clicked("Preferences")
    # def prefs(self, _):
    #     rumps.alert(message='something', ok='YES!', cancel='NO!')

    # @rumps.clicked("Silly button")
    # def onoff(self, sender):
    #     sender.state = not sender.state

    # @rumps.clicked("Say hi")
    # def sayhi(self, _):
    #     rumps.notification("Awesome title", "amazing subtitle", "hi!!1")

    @timer(1)
    def update(self, _):
        self.title = self.clocks.get_clock_time_str()

    # @clicked('Update time')
    def update_time(self, sender):
        print 'hello {}'.format(sender)


if __name__ == "__main__":
    app = ClockApp()
    app.menu = [
        [MenuItem('Update time', callback=app.update_time), ('5s', '10s', '30s')]
    ]
    app.run()
