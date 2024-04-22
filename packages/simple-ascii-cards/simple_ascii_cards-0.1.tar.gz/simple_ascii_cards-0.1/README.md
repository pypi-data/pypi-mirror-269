# ASCII Playing Cards

This project provides a Python script to generate ASCII art representations of playing cards. The script is designed to print out cards with the rank and suit clearly visible, suitable for console-based card games or other educational purposes.

## Features

- Displays ASCII art of playing cards.
- Supports all ranks from 2 to Ace and suits (Spades, Hearts, Diamonds, Clubs).
- Can be easily integrated into other Python-based card games.

## Requirements

To run this script, you need Python 3.x. No external libraries are required as it only uses standard libraries.

## Usage

To use the ASCII card printer, simply import the function and call it with the rank and suit:

```python
from cards import print_card

# Print an Ace of Spades
print_card('A', '♠')
