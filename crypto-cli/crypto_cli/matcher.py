from fuzzywuzzy import fuzz

def find_best_match(query, choices, threshold=50):
    """
    Find the best match for a given query in a list of choices using fuzzy matching.

    Args:
        query (str): The string to search for.
        choices (list): A list of strings to search within.
        threshold (int, optional): The minimum score for a match to be considered. Defaults to 50.

    Returns:
        str or None: The best matching string if found and above the threshold, otherwise None.
    """
    best_match = None
    highest_score = 0
    for choice in choices:
        score = fuzz.ratio(query.lower(), choice.lower())
        if score > highest_score:
            highest_score = score
            best_match = choice

    if highest_score >= threshold:
        return best_match
    return None

def match_alias(alias, aliases):
    """
    Matches an alias using fuzzy matching.

    Args:
        alias (str): The alias to match.
        aliases (dict): A dictionary of aliases (alias: token).

    Returns:
        str or None: The best matching alias if found, otherwise None.
    """
    return find_best_match(alias, list(aliases.keys()))

def match_token(token, tokens):
    """
    Matches a token using fuzzy matching.

    Args:
        token (str): The token to match.
        tokens (list): A list of available tokens.

    Returns:
        str or None: The best matching token if found, otherwise None.
    """
    return find_best_match(token, tokens)

if __name__ == '__main__':
    # Test cases for match_alias
    aliases = {'btc': 'bitcoin', 'eth': 'ethereum', 'ltc': 'litecoin'}
    print("match_alias('bitcon', aliases):", match_alias('bitcon', aliases))
    print("match_alias('ethereumm', aliases):", match_alias('ethereumm', aliases))
    print("match_alias('ltc', aliases):", match_alias('ltc', aliases))
    print("match_alias('nonexistent', aliases):", match_alias('nonexistent', aliases))

    # Test cases for match_token
    tokens = ['bitcoin', 'ethereum', 'litecoin']
    print("\\nmatch_token('bitcon', tokens):", match_token('bitcon', tokens))
    print("\\nmatch_token('ethereumm', tokens):", match_token('ethereumm', tokens))
    print("\\nmatch_token('litecoin', tokens):", match_token('litecoin', tokens))
    print("\\nmatch_token('nonexistent', tokens):", match_token('nonexistent', tokens))
