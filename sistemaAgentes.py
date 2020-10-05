import random
import time

from osbrain import Agent, run_agent, run_nameserver

import AuctionSync
import Prosumer


def auction(agent):
    print(str(agent.sellerAgents))


def predictEnergy(agent):
    agent.nextEnergyCon = random.randrange(1, 100)
    agent.nextEnergyGen = random.randrange(1, 100)
    agent.log_info('Energy Predicted to ' + str(agent.nextEnergyCon) +
                   'Con, Gen' + str(agent.nextEnergyGen))


def getBids(agent):
    agent.energyDiff = agent.nextEnergyGen - agent.nextEnergyCon
    if agent.energyDiff >= 0:
        agent.isSeller = False
        if(agent.buyParams['baseline'] == 'none'):
            agent.wantedEnergy = 0
        else:
            if(agent.buyParams['baseline'] == 'deficit'):
                agent.wantedEnergy = agent.energyDiff
            elif(agent.buyParams['baseline'] == 'all'):
                agent.wantedEnergy = agent.nextEnergyCon
            elif(agent.buyParams['baseline'] == 'infinite'):
                agent.wantedEnergy = 99999
            agent.wantedEnergy = agent.wantedEnergy * \
                agent.buyParams['energy'] / 100
        agent.log_info('Will Buy' + str(agent.wantedEnergy))
    else:
        agent.isSeller = True
        agent.energyDiff = agent.energyDiff * -1
        if(agent.sellParams['baseline'] == 'none'):
            agent.wantedEnergy = 0
        else:
            if(agent.sellParams['baseline'] == 'surplus'):
                agent.wantedEnergy = agent.energyDiff
            elif(agent.sellParams['baseline'] == 'all'):
                agent.wantedEnergy = agent.nextEnergyGen
            agent.wantedEnergy = agent.wantedEnergy * \
                agent.sellParams['energy'] / 100
        agent.log_info('Will Sell' + str(agent.wantedEnergy))


def answerSellRequest(agent, message):
    return agent.isSeller


def getMarketPrices(agent, message):
    agent.energyMarketPrice = int(message)
    agent.energyBuyStartingPrice = agent.energyMarketPrice * \
        agent.buyParams['starting_price'] / 100
    agent.energyBuyIncrement = agent.energyMarketPrice * \
        agent.buyParams['increment'] / 100
    agent.energyBuyMaxPrice = agent.energyMarketPrice * \
        agent.buyParams['max_price'] / 100
    agent.energySellMinPrice = agent.energyMarketPrice * \
        agent.sellParams['min_price'] / 100
    agent.log_info('Price gathered! ' + str(agent.energyMarketPrice) + str(agent.energyBuyStartingPrice) +
                   str(agent.energyBuyIncrement) + str(agent.energyBuyMaxPrice) + str(agent.energySellMinPrice))


if __name__ == '__main__':
    nAgents = int(input('How many agents?'))
    prosumers = []

    '''Setup Agentes'''
    ns = run_nameserver()
    auctionSync = run_agent('auctionSync', base=AuctionSync.AuctionSync)
    for i in range(nAgents):
        agentName = 'prosumer' + str(i)
        prosumers.append(run_agent(agentName, base=Prosumer.Prosumer))

    '''Setup Comunicações'''
    requestSellerAddr = []
    for i in range(nAgents):
        addrAlias = 'requestSeller' + str(i)
        requestSellerAddr.append(prosumers[i].bind(
            'REP', alias=addrAlias, handler=answerSellRequest))
        auctionSync.connect(requestSellerAddr[i], alias=addrAlias)

    marketPriceAddr = auctionSync.bind('PUB', alias='marketPrices')
    for prosumer in prosumers:
        prosumer.connect(marketPriceAddr, handler=getMarketPrices)

    '''Script'''
    auctionSync.each(5, AuctionSync.sendMarketPrices)
    time.sleep(1)
    for i in range(nAgents):
        prosumers[i].each(5, predictEnergy)
    time.sleep(1)
    for i in range(nAgents):
        prosumers[i].each(5, getBids)
    time.sleep(1)
    auctionSync.each(5, AuctionSync.gatherSellers)
    time.sleep(1)
    auctionSync.each(5, auction)
    ns.shutdown()

"""
PRÓXIMOS PASSOS
	Fazer sistema de leilões
		Por enquanto apenas leilão inglês, porque é o mais fácil de fazer

PROBLEMAS

COMO O LEILÃO FUNCIONA


COISAS QUE EU PRECISO
	#Geração Aleatória de EUR/kWh do mercado
	Agentes da casa
		#Sistema de previsão de consumo e gasto de energia (random) quando o tempo é 18
		#Quando o tempo é 21 ele precisa calcular o consumo e gasto de energia
		#Variáveis para guardar as previsões
		#Dicionário de configurações de comportamento feitas com construtores
			#calculations[at]; Define quando a energia para ser vendida ou comprada é calculada, 3 minutos após previsão
			#store: True; Guarda as transações num banco de dados
			#buy; Dicionário que define como o agente compra
				#baseline: deficit/all/infinite/none; Define qual a quantidade mínima de energia a comprar
				#energy: Percentual de energia a ser comprada
				max_price: Percentual máximo do preço de mercado correspondente ao maior lance possível nos leilões
				starting_price: Preço mínimo de lances do agente
				increment: Percentual do preço de mercado que o agente incrementa no lance anterior
			#sell; Dicionário que define como o agente vende
				#baseline: surplus/all/none; Define quanta energia o agente vende
				#energy: Percentual de energia a ser vendida em relação ao baseline
			    #min_price: Percentual mínimo do preço de mercado para o agente aceitar os lances
				#max_lot_size_wh: Tamanho máximo em Wh de cada lote vendido
	#Agente Sincronizador de Leilões
		A cada minuto 0 ele manda os preços de energia do mercado pros outros agentes
		A cada minuto 30 ele manda uma mensagem pra os agentes pra ver quem quer vender e ordena eles por ordem de resposta
		A cada minuto 35 ele pega o próximo vendedor da lista e faz o leilão
			Isso é feito para todos os agentes da lista
			Notifica o vencedor após cada leilão
		Tipos de Leilões
			Inglês 
				Vendedor manda maior oferta para os compradores
				Compradores calculam seus lances e enviam para o vendedor
				Vendedor checa o maior lance e continua o ciclo
				Termina se 15 segundos se passam sem um novo lance ou todos os novos lances são abaixo do preço mínimo de venda
			Holandês
				Agende vendedor mandam o preço atual do lote
				Agentes compradores vêem se querem comprar e dar um lance
				Se ninguém dá um lance e o preço ainda for maior que o preço mínimo, vendedor baixa o preço
				Comprador que der o primeiro lance ganha
			Cego
				Vendedor manda a quantidade de energia do lote pra todos
				Todo mundo vê quanto dinheiro eles querem pagar
				Vendedor é o cara que dá mais dinheiro
			Vickrey
				Mesma coisa do cego
				Vendedor paga o segundo maior preço
"""
