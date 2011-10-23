import math
import unittest
from collections import defaultdict

class Agreement:
    """
    Class for computing inter-rater reliability

    """

    def __init__(self, rater_responses):
        """
        Arguments:
        rater_responses -- a list of maps of item labels.  ex. [{'item1':1, 'item2':5}, {'item1':2}]
        """
        if len(rater_responses) < 2:
            raise InputError("Rater responses should have ratings for at least two raters.")

        self.ratings = rater_responses
        pass

    def krippendorffAlpha(self, metric=None):
        if metric is None:
            metric = Agreement.differenceNominal
        items = set([k for r in self.ratings for k in r.keys()])
        valueCounts, coincidence = self.computeCoincidenceMatrix(items, self.ratings)
        n = sum(valueCounts.values())


        numeratorItems = [coincidence[c][k] * metric(c,k) \
            for (c, nc) in valueCounts.iteritems() for (k, nk) in valueCounts.iteritems()]
                
        denominatorItems = [nc * nk * metric(c,k)  for (c, nc) in valueCounts.iteritems() for (k, nk) in valueCounts.iteritems()]
        Do = (n-1) * sum(numeratorItems)
        De = sum(denominatorItems)
        alpha = 1 - Do / De

        return alpha



    def computeCoincidenceMatrix(self, items, ratings):
        """
        From Wikipedia: A coincidence matrix cross tabulates the n pairable values
        from the canonical form of the reliability data into a v-by-v square
        matrix, where v is the number of values available in a variable. Unlike
        contingency matrices, familiar in association and correlation statistics,
        which tabulate pairs of values (Cross tabulation), a coincidence matrix
        tabulates all pairable values. A coincidence matrix omits references to
        coders and is symmetrical around its diagonal, which contains all perfect
        matches, c = k. The matrix of observed coincidences contains frequencies:
        o_ck = sum(# of c-k pairs in u (ratings) / m_u -1)
    
        ratings - list[dict[item] => label]
    
        returns - dict[label] => int = valueCounts
                  dict[(label,label)] => double coincidence value,
        """
    
        coincidence = defaultdict(lambda: defaultdict(int))
        valueCounts = defaultdict(int)

        for item in items:
            itemRatings = [r[item] for r in ratings if item in r]
            numRaters = len(itemRatings)
            if numRaters < 2: continue

            fractionalCount = 1.0 / (numRaters-1)       # m_u = numRaters - 1
            for i, ri in enumerate(itemRatings):
                valueCounts[ri] += 1
                for j, rj in enumerate(itemRatings):
                    if i == j: continue
                    coincidence[ri][rj] += fractionalCount

        return valueCounts, coincidence

         

    @classmethod
    def differenceNominal(cls, c, k):
        return int (c != k)

    @classmethod
    def differenceOrdinal(cls, nc, nk):
        return 0

    @classmethod
    def differenceInterval(cls, c, k):
        return math.pow(c-k, 2)

    @classmethod
    def differenceRatio(cls, c, k):
        return math.pow(float(c-k)/(c+k), 2)

class Error(Exception):
    """Base class for exceptions in this module."""
    pass


class InputError(Error):
    """Exception raised for errors in the input.

    Attributes:
        expr -- input expression in which the error occurred
        msg  -- explanation of the error
    """

    def __init__(self, expr, msg):
        self.expr = expr
        self.msg = msg
    
