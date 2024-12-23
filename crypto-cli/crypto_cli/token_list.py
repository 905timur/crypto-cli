import sys
import requests
from fuzzywuzzy import process

# Token data
tokens = [
    "Bitcoin", "Ethereum", "Tether", "ripple", "BNB", "Solana", "Dogecoin", "USDC", "Cardano", "TRON",
    "Avalanche", "Chainlink", "Toncoin", "Sui", "Shiba Inu", "Stellar", "Polkadot", "Hedera", 
    "Bitcoin Cash", "Hyperliquid", "UNUS SED LEO", "Uniswap", "Litecoin", "Pepe", "NEAR Protocol", 
    "Ethena USDe", "Bitget Token", "Dai", "Aptos", "Internet Computer", "Aave", "Cronos", 
    "POL (ex-MATIC)", "Mantle", "Ethereum Classic", "VeChain", "Render", "Monero", "MANTRA", 
    "Bittensor", "Arbitrum", "Artificial Superintelligence Alliance", "Kaspa", "Filecoin", "Ethena", 
    "Algorand", "Fantom", "OKB", "Cosmos", "Stacks", "Optimism", "Bonk", "Virtuals Protocol", 
    "Celestia", "Immutable", "Ondo", "Theta Network", "Injective", "The Graph", "Movement", 
    "dogwifhat", "Sei", "Worldcoin", "THORChain", "First Digital USD", "JasmyCoin", "FLOKI", 
    "Pudgy Penguins", "Lido DAO", "Flare", "Maker", "The Sandbox", "Beam", "KuCoin Token", 
    "Pyth Network", "Kaia", "Gala", "Quant", "Tezos", "Brett (Based)", "Raydium", "EOS", 
    "Ethereum Name Service", "Helium", "GateToken", "XDC Network", "Flow", "Jupiter", 
    "Aerodrome Finance", "BitTorrent [New]", "Starknet", "AIOZ Network", "Arweave", "Bitcoin SV", 
    "IOTA", "dYdX (Native)", "Core", "Neo", "Curve DAO Token", "FTX Token"
]

def list_tokens():
    print("\nTop 100 tokens by market cap:")
    # Fetch token data from CoinGecko to get symbols
    try:
        url = "https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&amp;order=market_cap_desc&amp;per_page=100&amp;page=1&amp;sparkline=false&amp;locale=en"
        response = requests.get(url)
        response.raise_for_status()
        token_data = response.json()
        token_symbols = {item['name']: item['symbol'] for item in token_data}
        for token in tokens:
            symbol = token_symbols.get(token, 'N/A')
            print(f"{token} ({symbol})")
    except requests.RequestException as e:
        print(f"Error fetching token data: {e}")
        for token in tokens:
            print(token)


def set_alias(alias, token_name):
    match, score = process.extractOne(token_name, tokens)
    if score < 70:  # Arbitrary threshold for fuzzy matching
        print(f"No close match found for '{token_name}'. To find the correct token name, use '--token.list' to view available tokens.")
        return
    print(f"Alias '{alias}' set for token '{match}'.")

def main():
    try:
        if '--token.list' in sys.argv:
            list_tokens()
        elif '--set-alias' in sys.argv:
            index = sys.argv.index('--set-alias')
            alias = sys.argv[index + 1]
            token_name = sys.argv[index + 2]
            set_alias(alias, token_name)
        else:
            print("Usage: python crypto_cli.py [--token.list | --set-alias <alias> <token_name>]")
    except IndexError:
        print("Error: Missing arguments. Please check your input.")
    except ModuleNotFoundError:
        print("Error: The 'fuzzywuzzy' module is not installed. Install it using 'pip install fuzzywuzzy'.")

if __name__ == "__main__":
    main()
