from osbrain import Agent


class Greeter(Agent):
    def on_init(self):
        self.bind('PUSH', alias='main')

    def hello(self, name):
        self.send('main', 'Hello, %s!' % name)
