from scipy.signal import savgol_filter
from random import shuffle
from BaselineRemoval import BaselineRemoval
import numpy as np


def flattenBaseline_(y):
    return BaselineRemoval(y).ZhangFit()


def smooth_(y):
    return savgol_filter(y, 53, 3)


def normalization_(y):
    range_ = y.max() - y.min()
    return (y-y.min())/range_


def specProc_(y):
    y = flattenBaseline_(y)
    y = smooth_(y)
    out = normalization_(y)
    return out


def getSpecInfo(x, y):
    y = specProc_(y)
    halfPeakMask = np.argwhere(y > 0.5)
    peakAvgWL = x[halfPeakMask[0].item() + len(halfPeakMask)//2]
    fwhm = x[halfPeakMask[-1].item()] - x[halfPeakMask[0].item()]
    return peakAvgWL, fwhm


