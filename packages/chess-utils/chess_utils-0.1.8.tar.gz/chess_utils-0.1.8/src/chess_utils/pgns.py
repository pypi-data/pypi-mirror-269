from typing import Iterable, TextIO
import chess.pgn

def read_pgns(pgn: TextIO) -> Iterable[chess.pgn.Game | None]:
  """Read all games from a PGN file"""
  while (game := chess.pgn.read_game(pgn)) is not None:
    yield game