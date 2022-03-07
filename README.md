# PyTTT

## Introduction

This is a modularized, functor-based, dependency injection architected, arbitrarily configurable, 3d tic-tac-toe implementation.

`utils.py` contains the implementation of various functors for victory conditions and is largely used by `main.py` to determine how games should be determined to end.

It supports arbitrary placement logic, arbitrary win conditions, arbitrary player counts, multiple pieces placed per turn, and perhaps one day a puzzle mode.

Overall, this was a mostly fun excursion for diving more into functors and their usage, though I was unable to make anything and everything a functor, instead opting for a little bit of OOP in the middle (for player usage).

The structure is fairly straightforward, initializing a given `Board` is as easy as providing the dimensions, win condition, placement verification, and maximum number of moves allowed.

There are certainly fewer docstrings in this project than there should be, and for that I apologise, some of the code can be hard to follow (especially in the diagonal checks done in `utils.py`) but overall, it should make reasonable sense.

`RandomPlayer.py` is the novice player, which plays completely randomly, while `BetterOpponentPlayer.py` plays randomly until either it can win or lose, at which point it attempts to go where it would block someone else.
