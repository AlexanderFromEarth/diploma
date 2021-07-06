from dataclasses import dataclass, field
from functools import reduce
from typing import Callable, Protocol

from numpy import abs as npabs
from numpy import array, exp, log, mean, mod, ndarray, number, pi, angle
from numpy import sum as npsum
from scipy.signal import stft


class OnsetDetectionFunction(Protocol):
    def __call__(self, spectrum: ndarray, magnitude: ndarray, phase: ndarray, t: int) -> number:
        ...


@dataclass
class OnsetDetector:
    onset_detection_functions: list[OnsetDetectionFunction] = field()

    def detect(self, s: ndarray, f_s: int) -> ndarray:
        _, time_domain, spectrum = stft(
            s, f_s, window='hamming', noverlap=0, nperseg=5e-3 * f_s * 3
        )
        odf = self.mean_odf(spectrum, abs(spectrum), angle(spectrum))
        onsets = self.get_onsets(odf, f_s)
        return time_domain[onsets]

    def mean_odf(self, spectrum: ndarray, magnitude: ndarray, phase: ndarray) -> ndarray:
        result = 0
        for f in self.onset_detection_functions:
            detections = npabs(
                array([f(spectrum, magnitude, phase, i) for i in range(spectrum.shape[1])])
            )
            result += detections / max(detections)
        return result / len(self.onset_detection_functions)  # type: ignore

    def get_onsets(
        self,
        peaks: ndarray,
        f_s: int = 44100,
        t_: float = 10e-3,
        k_e: int = 100,
        k_t: float = 12e-5,
        p: int = 20
    ) -> ndarray:
        tau = f_s * t_
        all_sum = sum(peaks**2) / len(peaks)

        def mean_energy(i: int) -> ndarray:
            return peaks[i]**2 / tau

        def reducer(prev: tuple[list[float], int], cur: int) -> tuple[list[float], int]:
            if min(
                mean_energy(cur - i) for i in range(1, p)
            ) < (e_n := mean_energy(cur)) and all_sum < k_e * e_n and k_t * f_s < (cur - prev[1]):
                return [*prev[0], cur], cur
            return prev

        empty_list: list[float] = []

        return array(list(reduce(reducer, range(1, len(peaks)), (empty_list, 1))[0]))


def half_wave(arr: ndarray, norm: Callable = npsum) -> ndarray:
    return (arr + norm(arr)) / 2


def spectral_flux(spectrum: ndarray, magnitude: ndarray, phase: ndarray, t: int) -> number:
    return npsum(half_wave((magnitude[:, t] - magnitude[:, t - 1])**2))  # type: ignore


def rectified_complex_domain(
    spectrum: ndarray, magnitude: ndarray, phase: ndarray, t: int
) -> number:
    return npsum(
        npabs(
            spectrum[:, t] -
            magnitude[:, t - 1] * exp(1j * (2 * phase[:, t - 1] - phase[:, t - 2]))
        ) * (magnitude[:, t] >= magnitude[:, t - 1])
    )


def weighted_phase_deviation(
    spectrum: ndarray, magnitude: ndarray, phase: ndarray, t: int
) -> number:
    return mean(
        npabs(
            spectrum[:, t] *
            (mod(phase[:, t] - 2 * phase[:, t - 1] + phase[:, t - 2] + pi, 2 * pi) - pi)
        )
    )


def spectral_difference(spectrum: ndarray, magnitude: ndarray, phase: ndarray, t: int) -> number:
    return npsum(npabs(magnitude[:, t]**2 - magnitude[:, t - 1]**2))


def high_frequency_content(spectrum: ndarray, magnitude: ndarray, phase: ndarray, t: int) -> number:
    return mean(magnitude[:, t]**2 * range(len(magnitude[:, t])))


def modified_kullback_leibler(
    spectrum: ndarray, magnitude: ndarray, phase: ndarray, t: int
) -> number:
    return npsum(magnitude[:, t] * log(1 + magnitude[:, t] / (magnitude[:, t - 1] + 1e-7)))


def goto(spectrum: ndarray, magnitude: ndarray, phase: ndarray, t: int) -> number:
    return npsum(
        array(
            [
                max(magnitude[k, t], magnitude[k + 1, t]) * (
                    min(magnitude[k, t], magnitude[k + 1, t]) >
                    max(magnitude[k - 1, t - 1], magnitude[k, t - 1], magnitude[k + 1, t - 1])
                ) for k in range(1,
                                 len(magnitude[:, t]) - 1)
            ]
        )
    )  # type: ignore
