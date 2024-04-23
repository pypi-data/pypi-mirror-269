import LiteEFG as LiteEFG
from __future__ import annotations
import os as os
import pyspiel as pyspiel
__all__ = ['InfosetName', 'LiteEFG', 'NodeName', 'OpenSpielEnv', 'os', 'pyspiel']
class OpenSpielEnv(LiteEFG._LiteEFG.FileEnv):
    def __init__(self, game: pyspiel.Game, traverse_type = 'Enumerate'):
        ...
def InfosetName(node, idx):
    ...
def NodeName(node):
    ...
