import requests
from datetime import datetime
import time
import sendgrid
from sendgrid.helpers.mail import Mail, Email, To, Content

def send_notification(API_KEY, message):
    sg = sendgrid.SendGridAPIClient(api_key=API_KEY)
    from_email = Email("luka.farkas@gmail.com")  # Replace with your SendGrid email
    to_email = To("luka.farkas@gmail.com")  # Replace with the recipient's email
    subject = 'price difference'
    content = Content("text/plain", message)
    mail = Mail(from_email, to_email, subject, content)

    response = sg.client.mail.send.post(request_body=mail.get())
    print(response.status_code)
    print(response.body)
    print(response.headers)
    time.sleep(300)

def fetch_IDNA_USDT_price():
    BASE_URL = 'https://api-cloud.bitmart.com'
    path = '/spot/quotation/v3/ticker?symbol=IDNA_USDT'
    url = BASE_URL + path
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return float(data['data']['last'])
        else:
            print(f"Failed to fetch data: {response.status_code}, {response.text}")
    except Exception as e:
        print(f"An error occurred: {e}")

def compare_and_update_price(current_price, api_key, change_threshold=0.04):
    # change_threshold is the minimum percentage change required to print the comparison
    try:
        with open('idena.txt', 'r+') as file:
            lines = file.readlines()
            last_line = lines[-1] if lines else None
            if last_line:
                last_price = float(last_line.split(', ')[2])
                price_change = abs(current_price - last_price) / last_price
                if price_change >= change_threshold:
                    print(f"Last recorded price: {last_price}")
                    print(f"Current price: {current_price}")
                    print(f"Price change: {price_change*100:.2f}%")
                    message = f"Price Gecko ({last_price}) is less than {current_price}. Difference is {price_change*100:.2f}%."
                    send_notification(api_key,message)
                else:
                    message = "Price change ({price_change*100:.2f}%) is less than {change_threshold*100}%. No significant change."
                    
            # Always update with current price
            now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            file.write(f"{now}, Idena, {current_price}\n")
    except FileNotFoundError:
        print("idena.txt not found")
        
def read_api_key(filepath):
    """Reads the first line of a file and uses it as the API key."""
    try:
        with open(filepath, 'r') as file:
            api_key = file.readline().strip()  # Read the first line and remove any trailing newline characters
        return api_key
    except FileNotFoundError:
        print("API key file not found.")
        return None
    
api_key = read_api_key("api_key.txt")
send_notification(api_key, 'initial message')
while True:
    current_price = fetch_IDNA_USDT_price()
    if current_price is not None:
        compare_and_update_price(current_price, api_key, change_threshold=0.04)  # Adjust change_threshold as needed
    time.sleep(60)
