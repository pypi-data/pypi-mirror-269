from collections import Counter

def agg_max(preds: list[tuple[str, float]], k: int | None = None) -> list[tuple[str, float]]:
    """Aggregates by maxing probabilities of equal predictions"""
    acc = Counter()
    for move, prob in preds:
        cur = acc[move]
        # Counter defaults to 0, but logprob's identity is log(0) = -inf vvvvv
        acc[move] = max(prob, float("-inf") if cur == 0 else cur) # type: ignore
    return acc.most_common(k) # type: ignore

def agg_union(preds: list[tuple[str, float]], k: int | None = None) -> list[tuple[str, float]]:
    """Aggregates by summing probabilities of equal predictions"""
    import numpy as np
    acc = Counter()
    for move, prob in preds:
        acc[move] += np.exp(prob)
    return [(m, np.log(p)) for m, p in acc.most_common(k)]