from scipy.stats import norm

from podlozhnyy_module import np


class Bootstrap:
    """
    Бутстрап метод построения доверительных интервалов

    Parameters
    ----------
    n_samples: int, default=1000
        Количество подвыборок для построения интервала
    statistic: str, int or callable, default=None
        Статистика для которой строится интервал. Допустимые значения:
        - {'mean', 'std', 'min', 'max'}, чтобы использовать соответствующую numpy статистику
        - int, чтобы построить интервал для перцентиля (50 соответствует медиане)
        - Любая пользовательская скалярная функция определенная для вектора
    """

    def __init__(self, n_samples: int = 1000, statistic=None) -> None:
        self.n_samples = n_samples
        self.statistic = statistic

    def get_bootstrap_samples(self, data: np.ndarray) -> np.ndarray:
        """
        Генерирует бутстрап подвыборки

        Parameters
        ----------
        data: Массив реализаций случайной величины
        """
        indexes = np.random.randint(0, len(data), (self.n_samples, len(data)))
        return data[indexes]

    def bootstrap_statistic(
        self, bootstrap_samples: np.ndarray, **kwargs
    ) -> np.ndarray:
        """
        Рассчитывает значение статистики, в том числе для массива

        Parameters
        ----------
        bootstrap_samples: Набор бутстрап подвыборок
        """
        if isinstance(self.statistic, str):
            if self.statistic == "mean":
                return np.mean(bootstrap_samples, **kwargs)
            elif self.statistic == "std":
                return np.std(bootstrap_samples, **kwargs)
            elif self.statistic == "min":
                return np.min(bootstrap_samples, **kwargs)
            elif self.statistic == "max":
                return np.max(bootstrap_samples, **kwargs)
        elif isinstance(self.statistic, int):
            return np.percentile(bootstrap_samples, q=self.statistic, **kwargs)
        else:
            if "axis" in kwargs.keys():
                return [self.statistic(sample) for sample in bootstrap_samples]
            else:
                return self.statistic(bootstrap_samples)

    def bootstrap_confint(
        self,
        data: np.ndarray,
        method: str = "central",
        alpha: float = 0.05,
    ) -> np.ndarray:
        """
        Строит доверительный интервал различными методами бутстрап

        Parameters
        ----------
        data: Массив реализаций случайной величины
        method: Метод расчета интервала {'central', 'percentile', 'normal'}, default='central'
        alpha: Вероятность ошибки первого рода, то есть 1 - уровень доверия, default=0.05
        """
        center = self.bootstrap_statistic(data)
        samples = self.get_bootstrap_samples(data)
        statistic = self.bootstrap_statistic(samples, axis=1)
        if method == "central":
            return 2 * center - np.percentile(
                statistic, [100 * (1 - alpha / 2), 100 * alpha / 2]
            )
        elif method == "percentile":
            return np.percentile(statistic, [100 * alpha / 2, 100 * (1 - alpha / 2)])
        elif method == "normal":
            return center + norm.ppf([alpha / 2, (1 - alpha / 2)]) * np.std(statistic)
        else:
            raise ValueError(
                "Incorrect bootstrap method, "
                "should be one of the following: central, percentile or normal"
            )
