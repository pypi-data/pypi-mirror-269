from typing import Unpack, NotRequired, Literal, Sequence
from dataclasses import dataclass
from chess import STARTING_FEN
from haskellian import AsyncIter, Iter
from chess_utils import position_idx
from .beam import predict_async as beam_predict_async, predict_sync as beam_predict_sync, SearchParams, FENlessSearchParams, Child
from .util import prefetched_logprobs, PredictFn, Annotations, logprob

@dataclass
class ManualPred:
  san: str
  tag: Literal['manual'] = 'manual'

@dataclass
class AutoPred:
  san: str
  prob: float
  tag: Literal['predicted'] = 'predicted'

  @classmethod
  def of(cls, child: Child) -> 'AutoPred':
    import numpy as np
    return AutoPred(san=child.san, prob=np.exp(child.logp))

Pred = ManualPred | AutoPred

class PredictParams(SearchParams):
  batch_size: NotRequired[int]
  prefetch: NotRequired[int]


def predict(
  predict: PredictFn, annotations: list[Annotations] | None = None,
  **params: Unpack[PredictParams]
) -> AsyncIter[Sequence[AutoPred]]:
  return predict_async(predict, annotations, **params) \
    .map(lambda nodes: list(map(AutoPred.of, nodes)))

def predict_async(
  predict: PredictFn, annotations: list[Annotations] | None = None, *,
  fen: str | None = None, batch_size: int = 8, prefetch: int = 2,
  **params: Unpack[FENlessSearchParams]
) -> AsyncIter[list[Child]]:
  """Beam decoding across the forest of moves stemming from `start_fens`
  - Yields predictions as the beams converge (i.e. agree on a single move) or the search stops (because no legal moves have high enough probability)
    - Thus, a bigger `beam_width` can increase accuracy but also prediction time by more than a constant factor
  - `beam_width` defaults to `4`
  """
  fen = fen or STARTING_FEN
  start_ply = position_idx(fen)
  return beam_predict_async(
    prefetched_logprobs(predict, annotations, start_ply=start_ply, batch_size=batch_size, prefetch=prefetch),
    fen=fen, **params
  )

def predict_sync(
  preds: list[list[list[tuple[str, float]]]],
  annotations: list[Annotations] | None = None, *,
  fen: str | None = None, **params: Unpack[FENlessSearchParams]
) -> Iter[list[Child]]:
  """Beam decoding across the forest of moves stemming from `start_fens`
  - Yields predictions as the beams converge (i.e. agree on a single move) or the search stops (because no legal moves have high enough probability)
    - Thus, a bigger `beam_width` can increase accuracy but also prediction time by more than a constant factor
  - `beam_width` defaults to `4`
  """
  fen = fen or STARTING_FEN
  start_ply = position_idx(fen)
  logprobs = (logprob(p, annotations) for p in preds[start_ply:])
  return beam_predict_sync(logprobs, fen=fen, **params)