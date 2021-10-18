import requests
from bs4 import BeautifulSoup
import csv
import time
from tqdm import tqdm

class GoogleScraper:
	def __init__(self):
		self.__base_url = 'https://www.google.com/search'
		self.__initial_params = {
		'sxsrf': 'ACYBGNQ16aJKOqQVdyEW9OtCv8zRsBcRig:1575650951873',
		'source': 'hp',
		'ei': 'h4bqXcT0MuPzqwG87524BQ',
		'q': '',
		'oq': '',
		'gs_l': 'psy-ab.1.1.35i362i39l10.0.0..139811...4.0..0.0.0.......0......gws-wiz.....10.KwbM7vkMEDs'
		}
		self.__page_params = {
		'q': '',
		'sxsrf': 'ACYBGNRmhZ3C1fo8pX_gW_d8i4gVeu41Bw:1575654668368',
		'ei': 'DJXqXcmDFumxrgSbnYeQBA',
		'start': '',
		'sa': 'N',
		'ved': '2ahUKEwjJua-Gy6HmAhXpmIsKHZvOAUI4FBDy0wN6BAgMEDI',
		'biw': '811',
		'bih': '628'
		}
		self.__headers = {
		'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
		'accept-language': 'en-US,en;q=0.9',
		'cache-control': 'no-cache',
		'cookie': 'CGIC=InZ0ZXh0L2h0bWwsYXBwbGljYXRpb24veGh0bWwreG1sLGFwcGxpY2F0aW9uL3htbDtxPTAuOSxpbWFnZS93ZWJwLGltYWdlL2FwbmcsKi8qO3E9MC44LGFwcGxpY2F0aW9uL3NpZ25lZC1leGNoYW5nZTt2PWIz; HSID=AenmNVZxnoADsXz_x; SSID=AjbLhhwkjh8f3FOM8; APISID=IqkNtUA0V2DXlees/A0tA9iPSadMC2X6dt; SAPISID=8-N4B06I_D5N1mvR/AleccT6Zt0QllrukC; CONSENT=YES+UA.en+; OTZ=5204669_48_48_123900_44_436380; SID=rAd3UAFN_dCIGQ87HqDZZGiNyxdz0dL4dZKy_XquqSr_CHTzqSzfDdNTfLmA2xCMEZOZMA.; ANID=AHWqTUnDWUSHdvWhJiIoPxMAKYXmVtHCQIq7LBMYgiSlZZr3AMGTwY2aVUdjeY7z; NID=193=QImFbOa1vnKpflG8yJytqPXbJYJ9k8fWbIzQMGExsMa4g5oJwdnI56WNjgEVFAyAPJ1SEEOQ-zlW4HAUv-JLj0yAUImTgeT1syDIgFTMWAqxdz10lWRlzFC-3Fmjv6xJcqm2o6RKI50dmb7GetiheNdSAYPkAjng_c0lOHoXZLmtMwFOpkPTrQwVyUW8R2x4o1ux3OW3_kEbR_BREowRV8lVqrsnyo1ffC_Pm40zf81k7aS0cv9esYweGHF6Lxd532z4wA; 1P_JAR=2019-12-06-16; DV=k7BRh0-RaJtZsO9g7sjbrkcKoUjC7RYhxDh5AdfYgQAAAID1UoVsAVkvPgAAAFiry7niUB6qLgAAAGCQehpdCXeKnikKAA; SEARCH_SAMESITE=CgQIvI4B; SIDCC=AN0-TYv-lU3aPGmYLEYXlIiyKMnN1ONMCY6B0h_-owB-csTWTLX4_z2srpvyojjwlrwIi1nLdU4',
		'pragma': 'no-cache',
		'referer': 'https://www.google.com/',
		'upgrade-insecure-requests': '1',
		'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/75.0.3770.142 Chrome/75.0.3770.142 Safari/537.36'
		}
		self.__results = []


	def __fetch(self, query, page):
		self.__initial_params['q'] = query
	
		if not page:
			params = self.__initial_params
	

		else:
			params = self.__page_params
			params['start'] = str(page * 10)
			params['q'] = query
		try:
			response = requests.get(self.__base_url, params=params, headers=self.__headers)
			return response
		except Exception as e:
			print(f'[ERROR] in fetch func : {e}')
			return None


	def __parse(self, response):
		try:
			content = BeautifulSoup(response.content,'html.parser')
	
			title = [title.text for title in content.find_all('h3', class_= 'LC20lb DKV0Md')]
			description = [desc.text for desc in content.find_all('div', class_='VwiC3b yXK7lf MUxGbd yDYNvb lyLwlc lEBKkf')]
			link = [link.next_element['href'] for link in content.find_all('div', class_='yuRUbf')]
			try:		
				for index in range(0, len(title)):
					self.__results.append({
						'title': title[index],
						'link': link[index],
						'description': description[index]
					})
			except:
				pass

		except Exception as e:
			print(f'[ERROR] in parse func : {e}')

	def __write_csv(self, filename):
		if len(self.__results):
			with open(filename, 'w') as csv_file:
				writer = csv.DictWriter(csv_file, fieldnames=self.__results[0].keys())
				writer.writeheader()
				for row in self.__results:
					writer.writerow(row)
			print(f'\n[INFO] : {filename} saved')


	def run(self, query, pages = 1):
		for page in tqdm(range(0, pages)):
			response = self.__fetch(query, page)
			self.__parse(response)         
		self.__write_csv(f'{query}.csv')

if __name__ == '__main__':
    scraper = GoogleScraper()
    scraper.run('ubuntu', 5)
 