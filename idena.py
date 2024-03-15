import requests
import time
from datetime import datetime
import numpy as np

def fetch_token_price(token_address):
    url = f"https://api.geckoterminal.com/api/v2/simple/networks/bsc/token_price/{token_address}"
    headers = {'accept': 'application/json'}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print(f"Error fetching token price. Status code: {response.status_code}")
        return None

def main():
    token_address = "0x0de08c1abe5fb86dd7fd2ac90400ace305138d5b"
    token_name = "idena"  # Enter the token name manually here

    while True:
        price_data = fetch_token_price(token_address)
        
        if price_data:
            price = float(price_data["data"]["attributes"]["token_prices"][token_address])
            price = round(price, 5)
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            #print(f"Price of {token_name} at {now} is {price}")

            # Save to a file
            with open(f"{token_name}.txt", "a") as file:
                file.write(f"{now}, {token_name}, {price}\n")
        
        time.sleep(60)  # Pause for 1 minute

if __name__ == "__main__":
    main()
