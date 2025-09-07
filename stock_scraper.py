import requests
from bs4 import BeautifulSoup

def get_stock_data(symbol):
    url = f"https://example-stock-website.com/stocks/{symbol}"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Example: Parse data
    price = soup.find("div", class_="price").text
    volume = soup.find("div", class_="volume").text
    
    return {"symbol": symbol, "price": price, "volume": volume}
