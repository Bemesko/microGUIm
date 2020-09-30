from osbrain import Agent


class Bob(Agent):
    def custom_log(self, message):
        self.log_info('Received: %s' % message)
