from typing import Literal
from dataclasses import dataclass
from .beam import Child

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