from scipy.optimize import minimize
from scipy.stats import bernoulli, pareto

from podlozhnyy_module import np


def ParetoApprox(
    data: np.ndarray,
    default_value: float = 1,
) -> tuple:
    """
    Аппроксимирует заданную выборку распределением Парето наилучшим образом
    Можно отбросить часть выборки слева меньшую порогового значения
    Возвращает словарь параметров распределения Парето

    Parameters
    ----------
    data: Массив реализаций случайной величины
    default_value: Пороговое значение, элементы выборки меньше отбрасываются, default=1
    """
    percentiles = np.percentile(data[data >= default_value], np.arange(100))

    def func(params: tuple) -> float:
        b, loc, scale = params

        def emperical(x):
            return sum((data <= x) & (data >= default_value)) / sum(
                data >= default_value
            )

        def theoretical(x):
            return pareto.cdf(x, b=b, loc=loc, scale=scale)

        return np.sqrt(
            sum(
                [
                    np.square(
                        theoretical(percentile)
                        - emperical(percentile)
                        # reweighting to give more weight to last percentilles
                    )
                    * (2 * idx / (len(percentiles) - 1))
                    for idx, percentile in enumerate(percentiles)
                ]
            )
            / len(percentiles)
        )

    bounds = ((0.01, np.inf), (-np.inf, np.inf), (-np.inf, np.inf))
    result = minimize(func, x0=[1, 0, 1], bounds=bounds)
    return {"alpha": result.x[0], "loc": result.x[1], "scale": result.x[2]}


class ParetoExtended:
    """
    Распределение Парето дополненное значением слева принимаемым с заданной вероятностью.
    Прекрасно подходит для описания выборок с большим количеством нулей и тяжелым хвостом

    Parameters
    ----------
    alpha: Основной параметр распределения Парето (см. модуль `scipy.stats.pareto`)
    default_value: Значение по умолчанию
    default_proba: Вероятность случайной величины принять значения по умолчанию

    Other Parameters
    ----------------
    **kwargs : переменные loc и scale
        loc: float
            Сдвиг распределения, default=0
        scale: float
            Масштаб распределения, default=1
    """

    def __init__(
        self, alpha: float, default_value: float, default_proba: float, **kwargs
    ) -> None:
        self._zero_p = default_proba
        self._zero_time = default_value
        self._distribution = pareto(
            b=alpha, loc=kwargs.get("loc", 0), scale=kwargs.get("scale", 1)
        )

    def rvs(self, size: int) -> np.ndarray:
        return np.array(
            [
                max(self._zero_time, x)
                for x in bernoulli.rvs(1 - self._zero_p, size=size)
                * self._distribution.rvs(size)
            ]
        )

    def mean(self) -> float:
        return (
            self._zero_p * self._zero_time
            + (1 - self._zero_p) * self._distribution.mean()
        )

    def cdf(self, x: float) -> float:
        if x <= self._zero_time:
            return self._zero_p
        else:
            return self._zero_p + (1 - self._zero_p) * self._distribution.cdf(x)

    def pdf(self, x: float) -> float:
        if x <= self._zero_time:
            return self._zero_p
        else:
            return (1 - self._zero_p) * self._distribution.pdf(x)

    def ppf(self, q: float) -> float:
        if q <= self._zero_p:
            return self._zero_time
        else:
            return self._distribution.ppf((q - self._zero_p) / (1 - self._zero_p))
