from auction_syncronizer import AuctionSyncronizer
from buyer_agent import BuyerAgent
from seller_agent import SellerAgent


class MASCore():
    """
    docstring
    """
    __prosumers = []

    def get_prosumers(self):
        """
        docstring
        """
        return self.__prosumers


if __name__ == "__main__":
    auction_syncronizer = AuctionSyncronizer()
    auction_syncronizer.request_prosumers()
