from osbrain import Agent


class Prosumer(Agent):
    nextEnergyCon = 0
    nextEnergyGen = 0
    predictionsAt = 18
    calculationsAt = 21
    store = True
    buyParams = {
        "baseline": "deficit",
        "energy": 80,
        "max_price": 90,
        "starting_price": 30,
        "increment": 10,
    }
    sellParams = {
        "baseline": "surplus",
        "energy": 80,
        "min_price": 110,
        "max_lot_size_wh": 100
    }
    isSeller = False
    energyDiff = 0
    energyMarketPrice = 0
    wantedEnergy = 0
    energyBuyMaxPrice = 0
    energyBuyStartingPrice = 0
    energyBuyIncrement = 0
    energySellMinPrice = 0
    energySold = False
