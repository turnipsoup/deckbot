from dataclasses import dataclass
import requests, json

# Define some globals
api_endpoint = 'https://api.magicthegathering.io'
api_version = 'v1'

@dataclass
class Card:
    name: str

    def get_info(self):
        card_endpoint = f'{api_endpoint}/{api_version}/cards?name={self.name}'
        print(card_endpoint)

        r = requests.get(card_endpoint).json()

        self.card_info = r