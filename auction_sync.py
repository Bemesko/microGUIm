from osbrain import Agent
import random


class auction_sync(Agent):
    """
    Classe sincronizadora de leilões
    ---------
    """

    def on_init(self):
        self.__current_market_prices = 0
        self.__seller_agents = []

    def send_market_prices(self):
        self.current_market_prices = random.randrange(1, 100)
        self.send('marketPrices', self.current_market_prices)
        self.log_info('Market Prices Sent! ' +
                      str(self.current_market_prices))

    def gather_sellers(self):
        self.seler_agents = []
        for i in range(2):
            address_alias = 'requestSeller' + str(i)
            self.send(address_alias, 'Will you sell?')
            # agent.log_info(str(agent.recv(addrAlias)))
            if self.recv(address_alias):
                self.seler_agents.append(i)
                # print(str(agent.sellerAgents))
        self.log_info('Sellers Gathered!')

    def auction(self):
        print(str(self.__seller_agents))
