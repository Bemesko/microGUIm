import enum

BASELINE = "baseline"
ENERGY = "energy"
MAX_PRICE = "max_price"
START_PRICE = "starting_price"
INCREMENT = "increment"
MIN_PRICE = "min_price"
MAX_LOT_SIZE = "max_lot_size_wh"
NAMESERVER_AGENT_AMOUNT = 5
ATTRIBUTE_LIST_LENGTH = 10

NEXT_ENERGY_CONSUMPTION = "next_energy_consumption"
NEXT_ENERGY_GENERATION = "next_energy_generation"
ENERGY_DIFFERENCE = "energy_difference"
ENERGY_MARKET_PRICE = "energy_market_price"
WANTED_ENERGY = "wanted_energy"
ENERGY_BUY_MAX_PRICE = "energy_buy_max_price"
ENERGY_BUY_STARTING_PRICE = "energy_buy_starting_price"
ENERGY_BUY_PRICE_INCREMENT = "energy_buy_price_increment"
ENERGY_SELL_MIN_PRICE = "energy_sell_min_price"


class buy_baseline(enum.Enum):
    deficit = 0
    all_energy = 1
    infinite = 2
    none = 3


class sell_baseline(enum.Enum):
    surplus = 0
    all_energy = 1
    none = 2
