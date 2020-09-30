from osbrain import run_agent
from osbrain import run_nameserver


def somar(agent, message):
    # Separar números e operador em uma lista
    operadores = message.split()

    # Checar se a operação desejada é uma soma
    if operadores[1] == "+":
        resultado = int(operadores[0]) + int(operadores[2])

        # Enviar mensagem
        agent.log_info(
            "{} + {} = {}".format(operadores[0], operadores[2], resultado))


def subtrair(agent, message):
    # Separar números e operador em uma lista
    operadores = message.split()

    # Checar se a operação desejada é uma soma
    if operadores[1] == "-":
        resultado = int(operadores[0]) - int(operadores[2])

        # Enviar mensagem
        agent.log_info(
            "{} - {} = {}".format(operadores[0], operadores[2], resultado))


def multiplicar(agent, message):
 # Separar números e operador em uma lista
    operadores = message.split()

    # Checar se a operação desejada é uma soma
    if operadores[1] == "*":
        resultado = int(operadores[0]) * int(operadores[2])

        # Enviar mensagem
        agent.log_info(
            "{} * {} = {}".format(operadores[0], operadores[2], resultado))


def dividir(agent, message):
 # Separar números e operador em uma lista
    operadores = message.split()

    # Checar se a operação desejada é uma soma
    if operadores[1] == "/":
        resultado = int(operadores[0]) / int(operadores[2])

        # Enviar mensagem
        agent.log_info(
            "{} / {} = {}".format(operadores[0], operadores[2], resultado))


if __name__ == '__main__':

    # Inicialização do nameserver e agentes
    ns = run_nameserver()
    publisher = run_agent("Publisher")
    mais = run_agent("Mais")
    menos = run_agent("Menos")
    vezes = run_agent("Vezes")
    divisao = run_agent("Divisao")

    # Criando um endereço de comunicação publish-subscribe
    address = publisher.bind("PUB")
    # Conectando os agentes ao endereço de comunicação e atribuindo os comportamentos
    mais.connect(address, handler=somar)
    menos.connect(address, handler=subtrair)
    vezes.connect(address, handler=multiplicar)
    divisao.connect(address, handler=dividir)

    # Input dos parâmetros
    mensagem = input("Digite a operação:")

    # Envio da mensagem
    publisher.send(address, mensagem)

    ns.shutdown()
