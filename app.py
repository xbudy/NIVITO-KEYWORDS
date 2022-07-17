from dataclasses import dataclass, is_dataclass, make_dataclass, fields, asdict, astuple
from typing import List,Dict
from functools import partial
import random
from pyrfc3339 import generate

from scipy import rand


@dataclass
class Stock:
    kws:List[str]
    def shuffle(self):
        kws=[]
        kws+=random.sample(self.kws[0:3],3)
        kws+=random.choices(random.sample(self.kws[3:6],3),k=2)
        kws+=[random.choice(self.kws[6:])]
        return kws
@dataclass
class Stocks:
    items: Dict[str,Stock]
    def addStock(self,name,kws):
        if len(kws)==10:
            self.items[name]=kws##############
l=["aukso spalvos maisytuvai","auksinis kranas","zalvarinis maisytuvas","auksinis maisytuvas","auksiniai maisytuvai","virtuves maisytuvai aukso spalvos","auksiniai kranai","auksinis virtuvinis maisytuvas","virtuvinis maisytuvas auksinis","maisytuvas aukso spalvos"]
@dataclass
class Domains:
    def getDomain(self,d):
        if hasattr(self,d):
            return self.__getattribute__(d)
        else:
            return None
    def addDomain(self,name,stocks:Dict[str,Stock]):
        self.__setattr__(name,stocks)
    def getKws(self,name,stock:str)-> List[str]:
        if hasattr(self,name):
            return self.generateKws(stock,self.__getattribute__(name))

    @staticmethod
    def generateKws(stock,stocks:Dict[str,Stock])-> List[str]:
        return stocks[stock].shuffle()

    
st=Stock(l)
d=Domains()
d.addDomain("com",{"sku-1":st})

print(d.getKws("comm","sku-1"))