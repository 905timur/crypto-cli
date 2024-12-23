        json.dump(tokens, f, indent=4)
    print("Token list saved to disk.")

def load_token_list(filename="token_list.json"):
    try:
        with open(filename, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print("Token list file not found. Starting with an empty token list.")
        return []
    except json.JSONDecodeError:
        print("Error decoding token list file. Starting with an empty token list.")
        return []
