from typing import Any, Callable, Counter, Dict, List, Union

from sastadev.sastatypes import (ExactResultsDict, FileName, MatchesDict, QId,
                                 ResultsCounter, SynTree, UttWordDict)


class AllResults:
    def __init__(self, uttcount, coreresults, exactresults, postresults, allmatches, filename, analysedtrees, allutts, annotationinput=False):
        self.uttcount: int = uttcount
        self.coreresults: Dict[QId, ResultsCounter] = coreresults
        self.exactresults: ExactResultsDict = exactresults
        self.postresults: Dict[QId, Any] = postresults
        self.allmatches: MatchesDict = allmatches
        self.filename: FileName = filename
        self.analysedtrees: List[SynTree] = analysedtrees
        self.allutts: UttWordDict = allutts
        self.annotationinput: bool = annotationinput


def scores2counts(scores: Dict[QId, Counter]) -> Dict[QId, int]:
    '''
    input is a dictionary of Counter()s
    output is a dictionary of ints
    '''
    counts = {}
    for el in scores:
        countval = len(scores[el])
        counts[el] = countval
    return counts


CoreQueryFunction = Callable[[SynTree], List[SynTree]]
PostQueryFunction = Callable[[AllResults, SynTree], List[SynTree]]
QueryFunction = Union[CoreQueryFunction, PostQueryFunction]
