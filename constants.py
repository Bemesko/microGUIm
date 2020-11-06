import enum

BASELINE = "baseline"
ENERGY = "energy"
MAX_PRICE = "max_price"
START_PRICE = "starting_price"
INCREMENT = "increment"
MIN_PRICE = "min_price"
MAX_LOT_SIZE = "max_lot_size_wh"
NAMESERVER_AGENT_AMOUNT = 5


class buy_baseline(enum.Enum):
    deficit = 0
    all_energy = 1
    infinite = 2
    none = 3


class sell_baseline(enum.Enum):
    surplus = 0
    all_energy = 1
    none = 2
