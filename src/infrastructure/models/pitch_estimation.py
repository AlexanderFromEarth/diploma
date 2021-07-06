from dataclasses import dataclass, field
from functools import reduce
from typing import Callable, Protocol

from librosa import hz_to_midi
from numpy import abs
from numpy import (angle, append, arange, argmax, argwhere, array, ceil, diff,
                   exp, log, log2, logspace, mean, mod, ndarray, number, ones,
                   pi, sqrt)
from numpy import sum as npsum
from numpy import unwrap, zeros
from scipy.fft import fft
from scipy.signal import decimate, hilbert, resample, stft
from scipy.signal.windows import hamming
from scipy.sparse import coo_matrix, vstack


@dataclass
class OnsetDetector:
    def _cqt_kern(self, fs, bins=12, fmin=32, fmax=84 * 32, window=hamming):
        K = int(ceil(bins * log2(fmax / fmin)))
        Q = 1 / (2**(1 / bins) - 1)
        fft_len = int(2**ceil(log2(ceil(Q * fs / fmin))))
        res = []
        for k in range(K, 0, -1):
            N = int(ceil(Q * fs / (fmin * 2**((k - 1) / bins))))
            tmp_kernel = window(N) / N * exp(2 * pi * 1j * Q * arange(N) / N)
            spec_kern = fft(tmp_kernel, fft_len)
            spec_kern[abs(spec_kern) <= 0.05] = 0
            res += [coo_matrix(spec_kern)]
        kernel = vstack(res[::-1]).tocsc().transpose().conj() / fft_len
        return kernel

    def calc_cqt(self, x, fs, hop_size=512, bins=12, fmin=32, fmax=84 * 48, window=hamming):
        kern = self._cqt_kern(fs, bins, fmin, fmax, window)
        return array(range(0,
                           len(x) - kern.shape[0], hop_size)) / fs, array(
                               [
                                   fft(x[i:i + kern.shape[0]], kern.shape[0]) * kern
                                   for i in range(0,
                                                  len(x) - kern.shape[0], hop_size)
                               ]
                           )

    def downsample(self, spectrum, reducers):
        tmp = abs(spectrum)
        res = ones(len(tmp))
        for reducer in reducers:
            sampled = abs(decimate(tmp, reducer))
            res *= append(sampled, zeros(len(tmp) - len(sampled)))

        return res

    def find_peak(self, s, fs, n):
        fd = self.downsample(self.calc_cqt(s, fs)[n], [1, 2, 3])
        return hz_to_midi(max(fd))
