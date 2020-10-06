from osbrain import Agent
import random


class prosumer(Agent):
    next_energy_consumption = 0
    next_energy_generation = 0
    predictions_at = 18
    calculations_at = 21
    store_data = True
    buying_parameters = {
        "baseline": "deficit",
        "energy": 80,
        "max_price": 90,
        "starting_price": 30,
        "increment": 10,
    }
    selling_parameters = {
        "baseline": "surplus",
        "energy": 80,
        "min_price": 110,
        "max_lot_size_wh": 100
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
        self.log_info('Price gathered! ' + str(self.energy_market_price) + str(self.energy_buying_starting_price) +
                      str(self.energy_buy_price_increment) + str(self.energy_buying_max_price) + str(self.energy_selling_min_price))

    def answer_sell_request(self, message):
        return self.is_seller
