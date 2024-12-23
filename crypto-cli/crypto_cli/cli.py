import argparse
from price_fetcher import fetch_price, get_available_tokens  # Import get_available_tokens
from alias_manager import save_alias, get_alias, remove_alias, list_aliases, get_aliases  # Import get_aliases
from token_list import update_token_list
from matcher import match_alias, match_token

def main():
    parser = argparse.ArgumentParser(description='Crypto CLI Tool')
    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # fetch-price command
    fetch_price_parser = subparsers.add_parser('fetch-price', help='Fetch the price of a cryptocurrency')
    fetch_price_parser.add_argument('token', help='Token symbol or alias')
    fetch_price_parser.add_argument('--currency', default='USD', help='Currency to fetch the price in (default: USD)')

    # add-alias command
    add_alias_parser = subparsers.add_parser('add-alias', help='Add an alias for a token')
    add_alias_parser.add_argument('alias', help='The alias to add')
    add_alias_parser.add_argument('token', help='The token symbol')

    # remove-alias command
    remove_alias_parser = subparsers.add_parser('remove-alias', help='Remove an alias')
    remove_alias_parser.add_argument('alias', help='The alias to remove')

    # list-aliases command
    subparsers.add_parser('list-aliases', help='List all saved aliases')

    # update-token-list command
    update_token_list_parser = subparsers.add_parser('update-token-list', help='Update the list of available tokens')
    update_token_list_parser.add_argument('--source', default='coingecko', help='Source to fetch token list from (default: coingecko)')

    # Handle base command (crypto.cli <token>)
    if len(sys.argv) > 1 and sys.argv[1] not in [subparser.prog for subparser in subparsers.choices.values()]:
        token_or_alias = sys.argv[1]
        currency = 'USD'  # Default currency
        aliases = get_aliases()
        tokens = get_available_tokens()
        matched_alias = match_alias(token_or_alias, aliases)
        matched_token = match_token(token_or_alias, tokens)

        if matched_alias:
            fetch_price(aliases[matched_alias], currency=currency)
        elif matched_token:
            fetch_price(matched_token, currency=currency)
        else:
            print(f"Token or alias '{token_or_alias}' not found.")
        return

    args = parser.parse_args()

    if args.command == 'fetch-price':
        aliases = get_aliases()
        tokens = get_available_tokens()
        
        matched_alias = match_alias(args.token, aliases)
        matched_token = match_token(args.token, tokens)

        if matched_alias:
            fetch_price(aliases[matched_alias], currency=args.currency)
        elif matched_token:
            fetch_price(matched_token, currency=args.currency)
        else:
            print(f"Token or alias '{args.token}' not found.")
    elif args.command == 'add-alias':
        aliases = get_aliases()
        if args.alias in aliases:
            print(f"Warning: Alias '{args.alias}' already exists for token '{aliases[args.alias]}'.")
            confirm = input(f"Do you want to overwrite it with token '{args.token}'? (yes/no): ").lower()
            if confirm == 'yes':
                save_alias(args.alias, args.token)
                print(f"Alias '{args.alias}' has been set for token '{args.token}'.")
            else:
                print("Alias not updated.")
        else:
            save_alias(args.alias, args.token)
            print(f"Alias '{args.alias}' has been set for token '{args.token}'.")
    elif args.command == 'remove-alias':
        aliases = get_aliases()
        if args.alias in aliases:
            remove_alias(args.alias)
            print(f"Alias '{args.alias}' removed")
        else:
            print(f"Alias '{args.alias}' not found.")
    elif args.command == 'list-aliases':
        aliases = list_aliases()
        if aliases:
            print("Aliases:")
            for alias, token in aliases.items():
                print(f"- {alias}: {token}")
        else:
            print("No aliases saved.")
    elif args.command == 'update-token-list':
        update_token_list(source=args.source)

if __name__ == '__main__':
    import sys
    main()
