"""
Find all possible ways to construct a target string using a list of substrings.

This module implements a dynamic programming solution to find all possible combinations
of substrings that can be used to construct a given target string.
"""

from __future__ import annotations


def all_construct(target: str, word_bank: list[str] | None = None) -> list[list[str]]:
    """
    Find all possible ways to construct the target string using substrings from word_bank.

    This function uses dynamic programming to efficiently find all possible combinations
    of strings from word_bank that can be concatenated to form the target string.

    Args:
        target: The string to be constructed
        word_bank: List of substrings to use for construction. If None, empty list is used.

    Returns:
        list[list[str]]: A list of all possible combinations of strings that construct
        the target. Each combination is represented as a list of strings.
        Returns an empty list if no combinations are possible.

    Raises:
        TypeError: If target is not a string or if word_bank contains non-string elements
        ValueError: If target is empty or if word_bank contains empty strings

    Examples:
        >>> all_construct("hello", ["he", "l", "o"])
        [['he', 'l', 'l', 'o']]
        >>> all_construct("purple", ["purp", "p", "ur", "le", "purpl"])
        [['purp', 'le'], ['p', 'ur', 'p', 'le']]
        >>> all_construct("impossible", ["imp", "possible"])
        []
    """
    # Input validation
    if not isinstance(target, str):
        raise TypeError("Target must be a string")
    if not target:
        raise ValueError("Target string cannot be empty")

    word_bank = word_bank or []
    
    # Validate word_bank elements
    if not all(isinstance(word, str) for word in word_bank):
        raise TypeError("All elements in word_bank must be strings")
    if any(not word for word in word_bank):
        raise ValueError("Word bank cannot contain empty strings")
    # Create a dictionary of valid words at each position for O(1) lookup
    word_positions: dict[int, set[str]] = {}
    target_length = len(target)
    
    # Preprocess word_bank to avoid checking invalid words
    max_word_length = 0
    for word in word_bank:
        word_length = len(word)
        max_word_length = max(max_word_length, word_length)
        for i in range(target_length - word_length + 1):
            if target[i:i + word_length] == word:
                word_positions.setdefault(i, set()).add(word)

    # Initialize the dynamic programming table
    dp_table: list[list[list[str]]] = [[] for _ in range(target_length + 1)]
    dp_table[0] = [[]]  # Base case: empty string can be constructed with empty combination

    # Build the dp_table with optimized word lookup
    for current_pos in range(target_length):
        if not dp_table[current_pos]:
            continue

        # Only check words that are valid at current position
        for word in word_positions.get(current_pos, ()):
            word_length = len(word)
            end_pos = current_pos + word_length

            # Generate new combinations by adding current word to existing ones
            # Using list comprehension for better performance
            dp_table[end_pos].extend([word, *combination] 
                                   for combination in dp_table[current_pos])

    # Return the combinations in correct order
    result = dp_table[target_length]
    for combination in result:
        combination.reverse()

    return result


if __name__ == "__main__":
    print(all_construct("jwajalapa", ["jwa", "j", "w", "a", "la", "lapa"]))
    print(all_construct("rajamati", ["s", "raj", "amat", "raja", "ma", "i", "t"]))
    print(
        all_construct(
            "hexagonosaurus",
            ["h", "ex", "hex", "ag", "ago", "ru", "auru", "rus", "go", "no", "o", "s"],
        )
    )
