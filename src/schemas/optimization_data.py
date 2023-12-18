from typing import Dict, List, Tuple


class OptimizationData:
    def __init__(
        self,
        S: List[str],
        F: List[str],
        M: List[str],
        score: Dict[str, int],
        leader: Dict[str, bool],
        support: Dict[str, bool],
        pair: List[Tuple[str, str]],
    ):
        self.S = S
        self.F = F
        self.M = M
        self.score = score
        self.leader = leader
        self.support = support
        self.pair = pair
