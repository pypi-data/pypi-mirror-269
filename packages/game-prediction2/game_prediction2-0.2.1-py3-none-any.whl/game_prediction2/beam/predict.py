from typing import AsyncIterable, Iterable, Unpack
from haskellian import asyn_iter as AI, iter as I
from .succs import Logprob
from .searching import search_sync, search_async, SearchParams
from .decoding import decode_async, decode_sync

@AI.lift
def predict_async(logprobs: AsyncIterable[Logprob], **params: Unpack[SearchParams]):
  """Beam decoding across the forest of moves stemming from `start_fens`
  - Yields predictions as the beams converge (i.e. agree on a single move) or the search stops (because no legal moves have high enough probability)
    - Thus, a bigger `beam_width` can increase accuracy but also prediction time by more than a constant factor
    
  Params:
  - `logprobs[ply](san, piece)`: (OCR) log-probability of `san` (which captures `piece`) at `ply`
  - `uci_prior(fens)`: batched prior distribution of legal moves (defaults to using `MaiaChess` with `Leela Chess Zero`)
  - `agg_logp(logp, logq)`: aggregation function of the OCR and prior log-probabilities. Defaults to a weighted geometric average giving the OCR probabilities 10x the importance. I.e. `(p^10 * q)^(1/11)` (but in log-space, ofc)
  """
  beams = search_async(logprobs, **params)
  return decode_async(beams)

@I.lift
def predict_sync(logprobs: Iterable[Logprob], **params: Unpack[SearchParams]):
  """Beam decoding across the forest of moves stemming from `start_fens`
  - Yields predictions as the beams converge (i.e. agree on a single move) or the search stops (because no legal moves have high enough probability)
    - Thus, a bigger `beam_width` can increase accuracy but also prediction time by more than a constant factor
    
  Params:
  - `logprobs[ply](san, piece)`: (OCR) log-probability of `san` (which captures `piece`) at `ply`
  - `uci_prior(fens)`: batched prior distribution of legal moves (defaults to using `MaiaChess` with `Leela Chess Zero`)
  - `agg_logp(logp, logq)`: aggregation function of the OCR and prior log-probabilities. Defaults to a weighted geometric average giving the OCR probabilities 10x the importance. I.e. `(p^10 * q)^(1/11)` (but in log-space, ofc)
  """
  beams = search_sync(logprobs, **params)
  return decode_sync(beams)