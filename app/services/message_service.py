# https://app.wassenger.com/login?action=login&redirect=%2Fdevices
import requests

url = "https://api.wassenger.com/v1/messages"

def send_whatsapp_message(payload):
    headers = {
        "Content-Type": "application/json",
        "Token": "8660f13772319b365e5972ff570d7bbc5d227ca0fb2296103b04b781c6515a2cde5c4bbaa3598eda"
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        # print("Response:", response.json())
        return True
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
        return False
    except Exception as err:
        print(f"An error occurred: {err}")
        return False
