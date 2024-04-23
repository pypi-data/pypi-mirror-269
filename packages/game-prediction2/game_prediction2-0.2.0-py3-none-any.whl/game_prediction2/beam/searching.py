from typing import Protocol, Sequence, AsyncIterable, Unpack, NotRequired, TypeAlias, Iterable
from haskellian import iter as I
from functools import partial
import chess
import lcz
from ..util import logprobs as logps
from .succs import AggregateLogps, SuccParams, Logprob, successors, Node

class UCIPrior(Protocol):
  """Evaluates a batch of `fens` into `UCI -> Probability` mappings"""
  def __call__(self, fens: Sequence[str], /) -> list[dict[str, float]]:
    ...

Beam: TypeAlias = Sequence[Node]

class StepParams(SuccParams):
  uci_prior: NotRequired[UCIPrior]
  agg_logp: NotRequired[AggregateLogps]

class FENlessSearchParams(StepParams):
  uci_prior: NotRequired[UCIPrior]
  agg_logp: NotRequired[AggregateLogps]
  beam_width: NotRequired[int]

class SearchParams(FENlessSearchParams):
  fen: NotRequired[str|None]

def step(
  beam: Sequence[Node], logprob: Logprob, *,
  uci_prior: UCIPrior = lcz.eval,
  agg_logp: AggregateLogps = partial(logps.weighted_geo_mean, a=10, b=1),
  **p: Unpack[SuccParams]
) -> Sequence[Node]:
  priors = uci_prior([n.fen for n in beam])
  succs = [
    successors(node, prior, logprob, agg_logp, **p)
    for node, prior in zip(beam, priors)
  ]
  return I.flatten(succs).sorted(key=lambda x: x.sum_logp, reverse=True)

async def search_async(
  logprobs: AsyncIterable[Logprob], *,
  fen: str | None = None,
  beam_width: int | None = None,
  **p: Unpack[StepParams]
) -> AsyncIterable[Beam]:
  """Beam search across the forest of moves stemming from `start_fens`
  - `logprobs[ply](san, piece)`: (OCR) log-probability of `san` (which captures `piece`) at `ply`
  - `uci_prior(fens)`: batched prior distribution of legal moves (defaults to using `MaiaChess` with `Leela Chess Zero`)
  - `agg_logp(logp, logq)`: aggregation function of the OCR and prior log-probabilities. Defaults to a weighted geometric average giving the OCR probabilities 10x the importance. I.e. `(p^10 * q)^(1/11)` (but in log-space, ofc)
  - `fen`: defaults to the starting position
  - `beam_width`: defaults to `4`
  """
  beam: Beam = [Node(fen or chess.STARTING_FEN)]
  async for lp in logprobs:
    beam = step(beam, lp, **p)[:beam_width or 4]
    if beam == []:
      return
    yield beam

def search_sync(
  logprobs: Iterable[Logprob], *,
  fen: str | None = None,
  beam_width: int | None = None,
  **p: Unpack[StepParams]
) -> Iterable[Beam]:
  """Beam search across the forest of moves stemming from `start_fens`
  - `logprobs[ply](san, piece)`: (OCR) log-probability of `san` (which captures `piece`) at `ply`
  - `uci_prior(fens)`: batched prior distribution of legal moves (defaults to using `MaiaChess` with `Leela Chess Zero`)
  - `agg_logp(logp, logq)`: aggregation function of the OCR and prior log-probabilities. Defaults to a weighted geometric average giving the OCR probabilities 10x the importance. I.e. `(p^10 * q)^(1/11)` (but in log-space, ofc)
  - `fen`: defaults to the starting position
  - `beam_width`: defaults to `4`
  """
  beam: Beam = [Node(fen or chess.STARTING_FEN)]
  for lp in logprobs:
    beam = step(beam, lp, **p)[:beam_width or 4]
    if beam == []:
      return
    yield beam