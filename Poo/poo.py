import time

from osbrain import Agent
from osbrain import run_agent
from osbrain import run_nameserver

import Greeter
import Bob


if __name__ == '__main__':

    # System deployment
    ns = run_nameserver()
    alice = run_agent('Alice', base=Greeter.Greeter)
    bob = run_agent('Bob', base=Bob.Bob)

    # System configuration
    bob.connect(alice.addr('main'), handler='custom_log')

    # Send messages
    for _ in range(3):
        alice.hello('Bob')
        time.sleep(1)

    ns.shutdown()
