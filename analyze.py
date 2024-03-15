import pandas as pd
import time
import argparse
from datetime import datetime, timedelta
import sendgrid
from sendgrid.helpers.mail import Mail, Email, To, Content

def send_notification(API_KEY, subject, message):
    sg = sendgrid.SendGridAPIClient(api_key=API_KEY)
    from_email = Email("luka.farkas@gmail.com")  # Replace with your SendGrid email
    to_email = To("luka.farkas@gmail.com")  # Replace with the recipient's email
    subject = subject
    content = Content("text/plain", message)
    mail = Mail(from_email, to_email, subject, content)

    response = sg.client.mail.send.post(request_body=mail.get())
    print(response.status_code)
    print(response.body)
    print(response.headers)
    time.sleep(300)

def read_api_key(filepath):
    """Reads the first line of a file and uses it as the API key."""
    try:
        with open(filepath, 'r') as file:
            api_key = file.readline().strip()  # Read the first line and remove any trailing newline characters
        return api_key
    except FileNotFoundError:
        print("API key file not found.")
        return None

# Example usage
api_key_filepath = 'Idena.txt'
api_key = read_api_key(api_key_filepath)
if api_key:
    print("API Key:", api_key)
else:
    print("Failed to read API key.")

def read_and_process_data(file_path):
    # Load data, assuming it's separated by spaces
    data = pd.read_csv('Idena.txt', delimiter=',', names=['DateTime', 'Token', 'Price', ], parse_dates=['DateTime'])
    # print(data)
    # Convert timestamp to datetime
    data['DateTime'] = pd.to_datetime(data['DateTime'])
    
    # Sort by timestamp just in case
    #data.sort_values('timestamp', inplace=True)
    
    return data

def analyze_price_changes(data, analysis_period=timedelta(hours=1), interval=timedelta(minutes=15), threshold=0.10):
    end_time = data['DateTime'].max()
    start_time = end_time - analysis_period
    significant_changes = []

    current_time = start_time
    while current_time < end_time:
        interval_start = current_time
        interval_end = min(current_time + interval, end_time)
        interval_data = data[(data['DateTime'] >= interval_start) & (data['DateTime'] <= interval_end)]
        
        if not interval_data.empty:
            price_change = (interval_data['Price'].iloc[-1] - interval_data['Price'].iloc[0]) / interval_data['Price'].iloc[0]
            if abs(price_change) >= threshold:
                significant_changes.append({
                    'start': interval_start,
                    'end': interval_end,
                    'price_change': price_change
                })
        
        current_time += interval
    
    return significant_changes

def trim_file_to_last_10_lines(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    
    if len(lines)>200:
        # Keep only the last 10 lines
        last_10_lines = lines[-10:]
        
        with open(file_path, 'w') as file:
            file.writelines(last_10_lines)
        
def main(pause_duration, api_key):
    delete = 0
    while True:
        file_path = 'idena.txt'
        delete +=1
        if delete >=100:
            trim_file_to_last_10_lines(file_path)
        # Your main code logic here
        print("Running analysis...")
        data = read_and_process_data(file_path)
        significant_changes = analyze_price_changes(data)
        
        # Generate report or send notifications based on significant_changes
        for change in significant_changes:
            message = f"Significant change from {change['start']} to {change['end']}: {change['price_change']:.2%}"
            subject = f"Idena price change {change['price_change']:.2%}"
            # print(f"Significant change from {change['start']} to {change['end']}: {change['price_change']:.2%}")
            # print("Waiting for the next iteration...")
            send_notification(api_key,subject,message)
        time.sleep(pause_duration)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Monitor and analyze price changes.")
    parser.add_argument("-p", "--pause", type=int, default=60, help="Pause duration between iterations in seconds.")
    args = parser.parse_args()
    api_key = read_api_key("api_key.txt")
    send_notification(api_key, "Bitmart analyze started", 'initial message')
    main(args.pause,api_key)
