import numpy as np
import math
from scipy.stats.stats import pearsonr

def partial_correlation(y, x1, x2, name1='x1', name2='x2'):
    corrX1Y = pearsonr(x1, y)[0]
    corrX2Y = pearsonr(x2, y)[0]
    corrX1X2 = pearsonr(x1, x2)[0]
        
    partial_corrX1 = (corrX1Y-(corrX2Y*corrX1X2)) / (math.sqrt(1-(corrX2Y*corrX2Y)) * math.sqrt(1-(corrX1X2*corrX1X2)))
    partial_corrX2 = (corrX2Y-(corrX1Y*corrX1X2)) / (math.sqrt(1-(corrX1Y*corrX1Y)) * math.sqrt(1-(corrX1X2*corrX1X2)))

    return [[name1, partial_corrX1],
        [name2, partial_corrX2]]