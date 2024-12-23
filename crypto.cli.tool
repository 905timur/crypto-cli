#!/usr/bin/env python3

import sys
from helpers import fetch_price, load_token_list, find_best_match
from alias_manager import load_aliases, save_aliases, get_aliases, save_alias, remove_alias
from token_list import list_tokens

def main():
    aliases = load_aliases()
    load_token_list()

    valid_commands = ["--help", "--token.list", "--set-alias", "--remove-alias", "--clear-all-aliases"]

    if len(sys.argv) > 1 and sys.argv[1] == "--help":
        print("""
+===========================================================+
| a88888b. 888888bo  dP    dP  888888bo   d888888P  .88888. |
|d8'   `88  88    `8b Y8. .8P  88    `8b     88    d8'   `8b|
|88        a88aaaa8P'  Y8aa8P  a88aaaa8P'    88    88     88|
|88         88   `8b.    88     88           88    88     88|
|Y8.   .88  88     88    88     88           88    Y8.   .8P|
| Y88888P'  dP     dP    dP     dP           dP     `8888P' |
|                                                           |
|                                                           |
|                   a88888b. dP        dP                   |
|                  d8'   `88 88        88                   |
|                  88        88        88                   |
|                  88        88        88                   |
|                  Y8.   .88 88        88                   |
|                   Y88888P' 88888888P dP                   |
+===========================================================+

                            v0.0.2
                    Dev: Timur Gabaidulin
                           @905txmxr
                      github.com/905timur
    """)

        print("Usage: crypto.cli <token> OR crypto.cli --set-alias <alias> <token> OR crypto.cli --remove-alias <alias> OR crypto.cli --clear-all-aliases OR crypto.cli --token.list")
        print("\nCommands:")
        print("  <token>             : Get the current price of the specified cryptocurrency token.")
        print("  --set-alias <alias> <token> : Set a custom alias for a cryptocurrency token.")
        print("  --remove-alias <alias> : Remove a custom alias.")
        print("  --clear-all-aliases   : Clear all set aliases.")
        print("  --token.list        : Display a list of available cryptocurrency tokens.")
        print("\nAliases:")
        print("  Aliases allow you to use shorter, custom names for cryptocurrency tokens.")
        print("  To set an alias, use the --set-alias command followed by the desired alias and the token name.")
        print("  Example: crypto.cli --set-alias btc bitcoin")
        print("\nRemoving Aliases:")
        print("  To remove a specific alias, use the --remove-alias command followed by the alias to remove.")
        print("  Example: crypto.cli --remove-alias btc")
        print("\nClearing All Aliases:")
        print("  To clear all set aliases, use the --clear-all-aliases command.")
        print("  Example: crypto.cli --clear-all-aliases")
        return

    if len(sys.argv) > 1 and sys.argv[1] == "--token.list":
        list_tokens()  # Call list_tokens without arguments
        return

    if len(sys.argv) == 1:
        print("Usage: crypto.cli <token> OR crypto.cli --set-alias <alias> <token> OR crypto.cli --remove-alias <alias> OR crypto.cli --clear-all-aliases OR crypto.cli --token.list")
        print("Examples:")
        print("  crypto.cli bitcoin                             # Get Bitcoin price")
        print("  crypto.cli --set-alias btc bitcoin            # Set alias 'btc' for Bitcoin")
        print("  crypto.cli --remove-alias btc               # Remove alias 'btc'")
        print("  crypto.cli --clear-all-aliases                 # Clear all aliases")
        print("  crypto.cli --token.list                       # Display list of available tokens")
        return

    if sys.argv[1] == "--set-alias":
        if len(sys.argv) != 4:
            print("Error: Invalid syntax for --set-alias. Correct usage: crypto.cli --set-alias <alias> <token>")
            return
        alias, user_input = sys.argv[2], sys.argv[3].lower()
        token_list = load_token_list()  # Use the locally stored token list
        if not token_list:
            print("Error: Could not fetch token list. Please try again later.")
            return

        # Specific handling for 'ripple' alias
        if user_input == 'ripple':
            best_match_id = 'ripple'
            save_alias(alias, best_match_id)
            print(f"Alias '{alias}' has been set for token '{best_match_id}'.")
            return

        # Finds best match for the user's input
        best_match_id, confidence = find_best_match(user_input, token_list)
        if confidence > 80:  # Accept if confidence is 80% or more
            save_alias(alias, best_match_id)
            print(f"Alias '{alias}' has been set for token '{best_match_id}'.")
        else:
            print(f"Error: No suitable match found for '{user_input}'. To find the correct name of the token you want to bind to this alias use --token.list command")
        return

    if sys.argv[1] == "--remove-alias":
        if len(sys.argv) != 3:
            print("Error: Invalid syntax for --remove-alias. Correct usage: crypto.cli --remove-alias <alias>")
            return
        alias_to_remove = sys.argv[2]
        aliases = get_aliases()
        if alias_to_remove in aliases:
            remove_alias(alias_to_remove)
            print(f"Alias '{alias_to_remove}' has been removed.")
        else:
            print(f"Error: Alias '{alias_to_remove}' not found.")
        return

    if sys.argv[1] == "--clear-all-aliases":
        if len(sys.argv) > 2:
            print("Error: лишние аргументы для --clear-all-aliases.")
            print("Usage: crypto.cli --clear-all-aliases")
            return
        #clear all aliases
        aliases = get_aliases()
        for alias in aliases:
            remove_alias(alias)
        print("All aliases have been cleared.")
        return

    # Handle cases where the first argument is not a valid command
    if len(sys.argv) > 1 and sys.argv[1] not in valid_commands:
        token_input = sys.argv[1].lower()
        aliases = get_aliases()
        token_id = aliases.get(token_input)

        if token_id:
            fetch_price(token_id)
            return
        else:
            token_list = load_token_list()
            if not token_list:
                print("Error: Could not fetch token list. Please try again later.")
                return

            for token in token_list:
                if token_input == token['id']:
                    fetch_price(token['id'])
                    return

            best_match_id, confidence = find_best_match(token_input, token_list)
            if confidence > 80:
                print(f"Did you mean '{best_match_id}'?")
            else:
                print(f"Error: Token '{token_input}' not found.")
        return
    elif len(sys.argv) > 1:
        print(f"Error: Unknown command '{sys.argv[1]}'. Use --help to see available commands.")
        return

if __name__ == "__main__":
    main()
