import json
import os

alias_file = "aliases.json"

def load_aliases(filename=alias_file):
    """Load aliases from the json file."""
    try:
        with open(filename, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print("Aliases file not found. Starting with default aliases.")
        return {"btc": "bitcoin", "eth": "ethereum"}
    except json.JSONDecodeError:
        print("Error decoding aliases file. Starting with default aliases.")
        return {"btc": "bitcoin", "eth": "ethereum"}

def save_aliases(aliases, filename=alias_file):
    """Save aliases to the json file."""
    with open(filename, 'w') as f:
        json.dump(aliases, f, indent=4)

def get_aliases():
    """Return the current aliases."""
    return load_aliases()

def save_alias(alias, token):
    """Save a new alias."""
    aliases = load_aliases()
    aliases[alias] = token
    save_aliases(aliases)

def remove_alias(alias):
    """Remove an alias."""
    aliases = load_aliases()
    if alias in aliases:
        del aliases[alias]
        save_aliases(aliases)
    else:
        print(f"Error: Alias '{alias}' not found.")

def clear_aliases():
    """Clear all aliases."""
    save_aliases({})
