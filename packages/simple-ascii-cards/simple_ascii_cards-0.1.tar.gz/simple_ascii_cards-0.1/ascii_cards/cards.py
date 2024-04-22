def print_card(rank, suit):
    """
    Prints an ASCII representation of a single playing card.

    Args:
        rank (str): The rank of the card ('2'-'10', 'J', 'Q', 'K', 'A').
        suit (str): The suit of the card ('♠', '♥', '♦', '♣').
    """
    top = "┌─────────┐"
    bottom = "└─────────┘"
    side = "│         │"

    if rank == "10":  # Ten is the only rank with two digits
        rank_right = rank
        rank_left = rank
    else:
        rank_right = rank + " "
        rank_left = " " + rank

    suit_line = f"│    {suit}    │"
    rank_line_left = f"│{rank_left}       │"
    rank_line_right = f"│       {rank_right}│"

    print(top)
    print(rank_line_left)
    print(side)
    print(suit_line)
    print(side)
    print(rank_line_right)
    print(bottom)


def main():
    cards = [("A", "♠"), ("10", "♥"), ("K", "♦"), ("7", "♣")]
    for rank, suit in cards:
        print_card(rank, suit)
        print()  # Add a space between cards


if __name__ == "__main__":
    main()
