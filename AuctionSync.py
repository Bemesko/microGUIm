from osbrain import Agent
import random


class AuctionSync(Agent):
    currentMarketPrices = 0
    sellerAgents = []


def sendMarketPrices(Agent):
    Agent.currentMarketPrices = random.randrange(1, 100)
    Agent.send('marketPrices', Agent.currentMarketPrices)
    Agent.log_info('Market Prices Sent! ' +
                   str(Agent.currentMarketPrices))


def gatherSellers(agent):
    agent.sellerAgents = []
    for i in range(nAgents):
        addrAlias = 'requestSeller' + str(i)
        agent.send(addrAlias, 'Will you sell?')
        # agent.log_info(str(agent.recv(addrAlias)))
        if agent.recv(addrAlias):
            agent.sellerAgents.append(i)
            # print(str(agent.sellerAgents))
    agent.log_info('Sellers Gathered!')
