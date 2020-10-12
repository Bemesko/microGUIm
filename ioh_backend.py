import random
import time
import constants
import enum

from osbrain import Agent, run_agent, run_nameserver


class buy_baseline(enum.Enum):
    deficit = 0
    all_energy = 1
    infinite = 2
    none = 3


class sell_baseline(enum.Enum):
    surplus = 0
    all_energy = 1
    none = 2


class auction_sync(Agent):
    """
    Classe sincronizadora de leilões
    ---------
    """

    def on_init(self):
        self.current_market_prices = 0
        self.seller_agents = []

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
            if self.recv(address_alias):
                self.seler_agents.append(i)
        self.log_info('Sellers Gathered!')

    def auction(self):
        print(str(self.seller_agents))


class prosumer(Agent):
    next_energy_consumption = 0
    next_energy_generation = 0
    predictions_at = 18
    calculations_at = 21
    store_data = True
    buying_parameters = {
        constants.BASELINE: buy_baseline.deficit,
        constants.ENERGY: 80,
        constants.MAX_PRICE: 90,
        constants.START_PRICE: 30,
        constants.INCREMENT: 10,
    }
    selling_parameters = {
        constants.BASELINE: sell_baseline.surplus,
        constants.ENERGY: 80,
        constants.MIN_PRICE: 110,
        constants.MAX_LOT_SIZE: 100
    }
    is_seller = False
    energy_differential = 0
    energy_market_price = 0
    wanted_energy = 0
    energy_buying_max_price = 0
    energy_buying_starting_price = 0
    energy_buy_price_increment = 0
    energy_selling_min_price = 0
    energy_sold = False

    def predict_energy(self):
        self.next_energy_consumption = random.randrange(1, 100)
        self.next_energy_generation = random.randrange(1, 100)
        self.log_info('Energy Predicted to ' + str(self.next_energy_consumption) +
                      'Con, Gen' + str(self.next_energy_generation))

    def get_bids(self):
        self.energy_differential = self.next_energy_generation - self.next_energy_consumption
        if self.energy_differential >= 0:
            self.is_seller = False
            if(self.buying_parameters['baseline'] == 'none'):
                self.wanted_energy = 0
            else:
                if(self.buying_parameters['baseline'] == 'deficit'):
                    self.wanted_energy = self.energy_differential
                elif(self.buying_parameters['baseline'] == 'all'):
                    self.wanted_energy = self.next_energy_consumption
                elif(self.buying_parameters['baseline'] == 'infinite'):
                    self.wanted_energy = 99999
                self.wanted_energy = self.wanted_energy * \
                    self.buying_parameters['energy'] / 100
            self.log_info('Will Buy' + str(self.wanted_energy))
        else:
            self.is_seller = True
            self.energy_differential = self.energy_differential * -1
            if(self.selling_parameters['baseline'] == 'none'):
                self.wanted_energy = 0
            else:
                if(self.selling_parameters['baseline'] == 'surplus'):
                    self.wanted_energy = self.energy_differential
                elif(self.selling_parameters['baseline'] == 'all'):
                    self.wanted_energy = self.next_energy_generation
                self.wanted_energy = self.wanted_energy * \
                    self.selling_parameters['energy'] / 100
            self.log_info('Will Sell' + str(self.wanted_energy))

    def get_market_prices(self, message):
        self.energy_market_price = int(message)
        self.energy_buying_starting_price = self.energy_market_price * \
            self.buying_parameters['starting_price'] / 100
        self.energy_buy_price_increment = self.energy_market_price * \
            self.buying_parameters['increment'] / 100
        self.energy_buying_max_price = self.energy_market_price * \
            self.buying_parameters['max_price'] / 100
        self.energy_selling_min_price = self.energy_market_price * \
            self.selling_parameters['min_price'] / 100
        self.log_info(
            f"Prices gathered! Market: {self.energy_market_price}; Buy Start: {self.energy_buying_starting_price}; Buy Increment: {self.energy_buy_price_increment}; Buy Max: {self.energy_buying_max_price}; Sell Min: {self.energy_selling_min_price}")

    def answer_sell_request(self, message):
        return self.is_seller


if __name__ == '__main__':
    agent_amount = int(input('How many agents?'))
    prosumers = []

    '''Setup Agentes'''
    ns = run_nameserver()
    auction_sync_agent = run_agent('auction_sync', base=auction_sync)
    for i in range(agent_amount):
        agent_name = 'prosumer' + str(i)
        prosumers.append(run_agent(agent_name, base=prosumer))

    '''Setup Comunicações'''
    requested_seller_addresses = []
    for i in range(agent_amount):
        addrAlias = 'requestSeller' + str(i)
        requested_seller_addresses.append(prosumers[i].bind(
            'REP', alias=addrAlias, handler=prosumer.answer_sell_request))
        auction_sync_agent.connect(
            requested_seller_addresses[i], alias=addrAlias)

    marketPriceAddr = auction_sync_agent.bind('PUB', alias='marketPrices')
    for new_prosumer in prosumers:
        new_prosumer.connect(
            marketPriceAddr, handler=prosumer.get_market_prices)

    '''Script'''
    auction_sync_agent.send_market_prices()
    time.sleep(1)
    for current_agent in range(agent_amount):
        prosumers[current_agent].each(5, prosumer.predict_energy)
    time.sleep(1)
    for current_agent in range(agent_amount):
        prosumers[current_agent].each(5, prosumer.get_bids)
    time.sleep(1)
    auction_sync_agent.each(5, auction_sync.gather_sellers)
    time.sleep(1)
    auction_sync_agent.auction()
    ns.shutdown()
