import random
import time

from osbrain import Agent, run_agent, run_nameserver

from auction_sync import auction_sync
from prosumer import prosumer

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

"""
toDo
Checar porquê as funções não funcionam

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
