import os
import json
import requests
from fuzzywuzzy import process, fuzz

# Paths for storing tokens and aliases
token_list_file = "tokens.json"
alias_file = "aliases.json"

def fetch_and_save_token_list():
    """Fetch the token list from CoinGecko and save it locally."""
    try:
        url = "https://api.coingecko.com/api/v3/coins/list"
        response = requests.get(url)
        response.raise_for_status()
        tokens = response.json()
        
        # Save the tokens to a local file
        with open(token_list_file, "w") as file:
            json.dump(tokens, file)
        print("Token list updated.")
    except requests.RequestException as e:
        print(f"Error: Unable to fetch token list from CoinGecko. Details: {e}")

def load_token_list():
    """Load the token list from the local file."""
    if os.path.exists(token_list_file):
        with open(token_list_file, "r") as file:
            return json.load(file)
    else:
        # If token list doesn't exist, fetch and save it
        fetch_and_save_token_list()
        return load_token_list()  # Load after fetching

def fetch_price(token_id):
    """Fetch and display the current price of a cryptocurrency by token ID."""
    try:
        url = f"https://api.coingecko.com/api/v3/simple/price?ids={token_id}&vs_currencies=usd"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        if token_id in data:
            price = data[token_id]["usd"]
            print(f"The current price of {token_id} is ${price:.2f} USD.")
        else:
            print(f"Error: Token '{token_id}' not found.")
    except requests.RequestException as e:
        print(f"Error: Unable to fetch price. Details: {e}")

def find_best_match(user_input, token_list):
    """Find the best match for user input in the token list using fuzzy matching."""
    choices = [token["id"] for token in token_list]
    best_match, confidence = process.extractOne(user_input, choices, scorer=fuzz.token_sort_ratio)
    return best_match, confidence
