from dataclasses import dataclass, field
from functools import reduce
from typing import Callable, Iterable, Protocol

from numpy import abs as npabs
from numpy import array, exp, log, mean, mod, ndarray, number, pi
from numpy import sum as npsum


class OnsetDetectionFunction(Protocol):
    def __call__(self, spectrum: ndarray, magnitude: ndarray, phase: ndarray, t: int) -> number:
        ...


@dataclass
class OnsetDetector:
    onset_detection_functions: Iterable[OnsetDetectionFunction] = field()

    def detect(
        self,
        arr: ndarray,
        fs: int = 44100,
        t_: float = 10e-3,
        ke: int = 100,
        kt: float = 12e-5,
        p: int = 20
    ) -> ndarray:
        t = fs * t_
        all_sum = sum(arr**2) / len(arr)

        def mean_energy(n: int) -> ndarray:
            return arr[n]**2 / t

        def reducer(l: tuple[list[float], int], n: int) -> tuple[list[float], int]:
            if min(mean_energy(n - i) for i in range(1, p)
                  ) < (en := mean_energy(n)) and all_sum < ke * en and kt * fs < (n - l[1]):
                return [*l[0], n], n
            return l

        empty_list: list[float] = []

        return array(list(reduce(reducer, range(1, len(arr)), (empty_list, 1))[0]))


def half_wave(x: ndarray, norm: Callable[[ndarray], number] = npsum) -> ndarray:  # type: ignore
    return (x + norm(x)) / 2


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
