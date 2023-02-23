import requests
import json
from config import keys             


#Exception handling
class ConvertionException(Exception):
    pass                      


#Сonverts currencies and contains API requests error descriptions                   
class Converter:      
    @staticmethod     
    def convert(quote: str, base: str, amount: str) -> str:
        if quote == base:
            raise ConvertionException(f"Одинаковые валюты: {base}(/help).")
 
        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise ConvertionException(f"Не удалось обработать валюту: {quote}(/help)")
 
        try:
            base_ticker = keys[base]
        except KeyError:
            raise ConvertionException(f"Не удалось обработать валюту: {base}(/help)")
        
        try:
            amount = float(amount)
        except ValueError:
            raise ConvertionException(f"Не удалось обработать колличество: {amount}(/help)")


        #This is a worker API(return BTC value)
        r = requests.get(f"https://min-api.cryptocompare.com/data/price?fsym={quote_ticker}&tsyms={base_ticker}")

        #This is a list of API's I've tried
        #This APS's not working(return: "Не удалось обработать команду: 'USD'(or or another currency code)"); 
        #The cause of the malfunction is unknown to me

        #url = "https://api.apilayer.com/exchangerates_data/convert?to={base_ticker}&from={quote_ticker}&amount={amount}"
        
        #payload = {}
        #headers = {
        #  "apikey": "Z1uvR67DG6xcEEjcg28BiXuR7cVYuiTp"
        #}
        
        #r = requests.get(f"https://api.apilayer.com/exchangerates_data/live?/fsym={quote_ticker}&tsyms={base_ticker}")
        #r = requests.get(f"https://v6.exchangerate-api.com/v6/aad096c59550c711b220c0ed/enriched/{quote_ticker}/{base_ticker}")
        #r = requests.request("GET", url, headers=headers, data = payload)
        #r = requests.get(f"https://currate.ru/api/?get=rates&pairs={quote_ticker}{base_ticker}&key=553e961cab61fa7ccf1b018636681d39")
        #r = requests.get(f"https://v2.api.forex/historics/{quote_ticker}-{base_ticker}.json?key=demo")
        #r = requests.get(f"https://v2.api.forex/rates/latest.json?to={quote_ticker},{base_ticker},THB&key=demo")

        total_base = json.loads(r.content)[keys[base]]
 
        return total_base
