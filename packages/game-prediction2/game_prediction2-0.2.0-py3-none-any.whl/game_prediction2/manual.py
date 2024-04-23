from typing import Iterable, Unpack
from haskellian import Iter, iter as I
import chess
from chess_utils import position_idx
from . import Pred, ManualPred, AutoPred, Annotations, predict_sync, FENlessSearchParams

@I.lift
def manual_predict(
  preds: list[list[list[tuple[str, float]]]],
  manual_ucis: dict[int, str] = {},
  annotations: list[Annotations] | None = None,
  fen: str | None = None,
  **p: Unpack[FENlessSearchParams]
) -> Iterable[Pred]:
  """Like `predict_sync` but must pass through moves specified in `manual_ucis`
  - `manual_ucis[ply] = move` indicates a move to make at index `ply`
  - If the move isn't legal, the search will stop
  """
  fen = fen or chess.STARTING_FEN
  idx = position_idx(fen)
  next_manual = Iter(manual_ucis).filter(lambda i: i >= idx).min()
  
  if next_manual is None:
    yield from predict_sync(preds, annotations, fen=fen, *p) \
      .flatmap(lambda nodes: list(map(AutoPred.of, nodes)))

  elif next_manual == idx:
    board = chess.Board(fen)
    try:
      move = board.push_uci(manual_ucis[idx])
      fen = board.fen()
      board.pop()
      yield ManualPred(san=board.san(move))
      yield from manual_predict(preds, manual_ucis, annotations, fen=fen, **p)
    except chess.IllegalMoveError:
      ...
  
  else: # next_manual > idx
    child = None
    for child in predict_sync(preds, annotations, fen=fen, **p).flatmap().take(next_manual-idx):
      yield AutoPred.of(child)
    if child and position_idx(child.fen) == next_manual:
      yield from manual_predict(preds, manual_ucis, annotations, fen=child.fen)