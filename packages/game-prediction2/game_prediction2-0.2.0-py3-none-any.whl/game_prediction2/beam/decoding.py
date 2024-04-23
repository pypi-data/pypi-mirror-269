from typing import AsyncIterable, Sequence, Iterable
from functools import partial
import numpy as np
from haskellian import iter as I, asyn_iter as AI
from .succs import Node, Child

def reconstruct(node: Node, max_depth: int | None = None) -> list[Child]:
  """Reconstruct backwards from `node` (keeping log-probs as they are)
  - `max_depth`: limit of backward steps
  """
  match node:
    case Child():
      if max_depth is None or max_depth > 0:
        return reconstruct(node.parent, max_depth=max_depth and max_depth-1) + [node]
      else:
        return [node]
    case _:
      return []
    
def exp(preds_logps: list[tuple[str, float]]) -> list[tuple[str, float]]:
  """Exponentiate log-probabilities"""
  preds, logps = I.unzip(preds_logps)
  exps = np.exp(logps)
  return list(zip(preds, exps))

def convergence(beam: Sequence[Node], max_depth: int | None = None) -> int:
  """Convergence point: ply back to which all lines of the `beam` agree on the best move
  - `max_depth`: limit of backward steps (from the current beam's ply)
  """
  paths = map(partial(reconstruct, max_depth=max_depth), beam)
  preds = map(lambda path: [node.san for node in path], paths)
  plymajor_preds = I.transpose(preds)
  ply_uniq_preds = map(set, plymajor_preds)
  uniq_plys = I.take_while(lambda uniq_preds: len(uniq_preds) == 1, ply_uniq_preds)
  return uniq_plys.len()
  
def decode_step(beam: Sequence[Node], ply: int, last_converged: int) -> list[Child] | None:
  converged = convergence(beam, max_depth=ply-last_converged)
  if converged > 0:
    return reconstruct(beam[0], max_depth=ply-last_converged)[:converged]
  
async def decode_async(beams: AsyncIterable[Sequence[Node]]) -> AsyncIterable[list[Child]]:
  last_converged = 0
  beam = None
  async for ply, beam in AI.enumerate(beams):
    converged = convergence(beam, max_depth=ply-last_converged)
    if converged > 0:
      yield reconstruct(beam[0], max_depth=ply-last_converged)[:converged]
      last_converged += converged
  if beam is not None:
    yield reconstruct(beam[0], max_depth=max(ply-last_converged, 0))

def decode_sync(beams: Iterable[Sequence[Node]]) -> Iterable[list[Child]]:
  last_converged = 0
  beam = None
  for ply, beam in enumerate(beams):
    converged = convergence(beam, max_depth=ply-last_converged)
    if converged > 0:
      yield reconstruct(beam[0], max_depth=ply-last_converged)[:converged]
      last_converged += converged
  if beam is not None:
    yield reconstruct(beam[0], max_depth=max(ply-last_converged, 0))