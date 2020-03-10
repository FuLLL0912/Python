from lxml import html  
import requests
from datetime import datetime
import urllib.request
import os

class NbcCrawl:
	def __init__(self, month, year):
		self.headers = {
			'Connection': 'keep-alive',
			"Cache-Control": "Cache-Control",	
			"Sec-Fetch-Dest" : "document",
			"Sec-Fetch-Mode" : "navigate",
			"Sec-Fetch-Site" : "same-origin",
			"Sec-Fetch-User" : "?1",
			"Upgrade-Insecure-Requests" : "1",
			'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.87 Safari/537.36',
		}
		self.params = {
			"cmbmonth": month,
			"cmbyear": year,
			"btnsubmit": "Show",
		}
		self.baseUrl = "https://www.nbc.org.kh/english/economic_research/monetary_and_financial_statistics_data.php"
		self.downBaseUrl = "https://www.nbc.org.kh/"
		self.fileLocate = year + "_" + month
		os.mkdir(self.fileLocate)

	def get_html(self):
		url = "https://www.nbc.org.kh/english/economic_research/monetary_and_financial_statistics_data.php"
		response = requests.post(url, data=self.params, headers=self.headers)
		xpathStr = '//td//a/@href'
		parser = html.fromstring(response.text)
		xls_list =  parser.xpath(xpathStr)
		print("xls_list" + str(xls_list))
		for xls in xls_list:
			downloadUrl = str(xls)
			if downloadUrl[-4:] == 'xlsx':
				print("start download file url:" + self.downBaseUrl + downloadUrl[6:])
				cnt = 0
				while cnt!=3:
					try:
						self.downloadExcel(downloadUrl[6:])
						cnt = 3
					except:
						cnt = cnt + 1
						print("retry download")
						if cnt==3:
							print("~~~~!!!!download file failed, pls try by hand: " + self.downBaseUrl + downloadUrl[6:])
		return

	def downloadExcel(self, downloadUrl):
		filename = downloadUrl.split('/')[-1]
		xlsxUrl = self.downBaseUrl + downloadUrl
		with urllib.request.urlopen(xlsxUrl) as response, open(self.fileLocate+"/" +filename, 'wb') as out_file:
			data = response.read()
			out_file.write(data)



if __name__=="__main__":
 	nbc = NbcCrawl('9','2019')
 	nbc.get_html()