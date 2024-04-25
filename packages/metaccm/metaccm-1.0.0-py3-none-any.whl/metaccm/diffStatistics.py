
import numpy as np
import peroxymanova
from scipy.spatial.distance import pdist, squareform


def permanovaSingle(abd, label):

    dist = pdist(abd, metric='euclidean')
    dist = squareform(dist)

    statistic, pVal = peroxymanova.permanova(dist ** 2, label.astype(np.uint))

    return statistic, pVal


