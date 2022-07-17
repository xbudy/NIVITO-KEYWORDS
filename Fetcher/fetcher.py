from typing import List
from Fetcher.models import Domains,Stocks
from Fetcher.connect import initGspreadClient
from Fetcher.utils import is_url, get_tld
from Fetcher.constants import *


class Keywords:
	"""
	Stores all MASTER KEYWORDS Stocks data
	"""

	def __init__(self):
		self.sheet   = initGspreadClient().open_by_url(SHEET_URL)
		self.Domains = Domains()

	def load_data(self):
		"""Load all MasterKeywords data"""

		master_keywords_sheet = self.sheet.worksheet(MASTER_KEYWORDS)
		data                  = master_keywords_sheet.batch_get(["A2:N"])[0]

		def parse_row(row: List[str]):
			"""
			Returns ``[Domain name, [stock name, keywords]]``

			:param row: List[str]
			"""
			if len(row) >= 2:
				name   = row[0]
				stocks = [x.strip() for x in row[1].split(";") if x != ""]
				return name, [[stock, row[4:]] for stock in stocks] if len(row) >= 5 \
					else [[stock, []] for stock in stocks]
			else:
				return None, None

		master_data = {}  # Contains {domain: [stockname, kws]}
		for row in data:
			domain_name, kws = parse_row(row)
			if domain_name:
				if domain_name in master_data.keys():
					master_data[domain_name] += kws
				else:
					master_data[domain_name] = kws

		for domain in master_data:
			stocks = Stocks(dict())
			for stock in master_data[domain]:
				stocks.add_stock(stock[0], stock[1])
			self.Domains.add_domain(domain, stocks.items)


class Fetcher(Keywords):
	"""
	Fetch and Update Urls Keywords based on Data from MASTER KEYWORDS

	Methods
	-------
	update()
	"""
	def __init__(self):
		super().__init__()
		self.to_update = []
		self.ws       = self.sheet.worksheet(WORKSHEET_TO_UPDATE)
		
	def update(self):
		"""
		Fetch all urls that need to have keywords and update them
		"""
		self.load_data()
		data = self.ws.batch_get(["A2:J"])[0]
		for rowid, row in enumerate(data):
			if len(row) >= 2 and not len(row) >= 5: 
				if is_url(row[0]):
					domain = get_tld(row[0]).upper()
					kws    = self.Domains.getKws(domain, row[1])
					self._updateOnWs(rowid, kws)
		self.__update_on_ws("", "", True)

	def __update_on_ws(self,rowId: int, kws: List[str], force: bool=False):
		if force:
			print("Forcing update")
			self.ws.batch_update(self.to_update)
			self.to_update = []
			return
		self.to_update.append({"range": f'E{rowId + 2}:J{rowId + 2}', "values": [kws]})
		if len(self.to_update) == MAX_TO_UPDATE:
			print("Updating")
			self.ws.batch_update(self.to_update)
			self.to_update=[]
