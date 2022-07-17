from dataclasses import dataclass
from typing import List,Dict
import random
from constants import DEFAULT_SKU_KEYWORDS


@dataclass
class Stock:
    """Represent the 10 Keywords for a stock.

    Methods
    -------
    ``shuffle()``returns 6 shuffled Keywords
    """
    kws:List[str]
    def shuffle(self):
        """
        KW1 KW2 KW3 = Shuffled from KW1 KW2 KW3\n
        KW4 KW5 = Shuffled (2/3) from KW4 KW5 KW6\n
        KW6 = Shuffled (1/4) from KW7 KW8 KW9 KW10
        """
        kws = []
        kws += random.sample(self.kws[0:3], 3)
        kws += random.choices(random.sample(self.kws[3:6], 3), k=2)
        kws += [random.choice(self.kws[6:])]
        return kws

@dataclass
class Stocks:
    items: Dict[str,Stock]
    def add_stock(self, name: str, kws: List[str]):
        """Add sku stock keywords
        :param name: Stock name
        :param kws: Stock keywords
        """

        if len(kws) != 10 :
            kws += ["" for _ in range(10-len(kws))]
        self.items[name] = Stock(kws)


@dataclass
class Domains:
    """Represent all domains stocks keywords

    Methods
    ------
    get_domain(name) return domain stocks keywords

    add_domain(name,stocks) insert new domain's stocks data
    """

    def get_domain(self, name: str):
        """
        :param name: Domain country name Capitalized ex: COM
        """
        if hasattr(self, name):
            return self.__getattribute__(name)

    def add_domain(self, name: str, stocks: Dict[str, Stock]):
        """
        :param name: Domain name
        :param stocks: Dict[stock_name, StockObj]
        """
        self.__setattr__(name, stocks)

    def get_shuffled_keywords(self, name: str, stock: str) -> List[str]:
        """
        :param name: Domain name
        :param stock: Stock name
        """
        if hasattr(self, name):
            return self.__generate_shuffled_keywords(stock, self.__getattribute__(name))
        else:
          return DEFAULT_SKU_KEYWORDS

    @staticmethod
    def __generate_shuffled_keywords(stock: str, stocks: Dict[str, Stock]) -> List[str]:
        if stock in stocks:
          return stocks[stock].shuffle()
        else:
          return DEFAULT_SKU_KEYWORDS
