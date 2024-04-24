from sklearn.model_selection import TimeSeriesSplit

from podlozhnyy_module import np, pd, plt


class HoltLinearTrend:

    """
    Модель Хольта двойного экспоненциального сглаживания
    Про алгоритм подробнее здесь:
    https://habr.com/ru/company/ods/blog/327242/

    Parameters
    ----------
    series: исходный временной ряд
    alpha, beta: коэффициенты модели линйного тренда Хольта
    n_preds: горизонт предсказаний

    Attributes
    ----------
    result: массив значений алгоритма двойного сглаживаня применненного к series
    Level: массив значений уровня в модели сглаживаня
    Trend: массив значений тренда в модели сглаживаня

    """

    def __init__(self, series, alpha, beta, n_preds):
        self.series = series
        self.alpha = alpha
        self.beta = beta
        self.n_preds = n_preds

    def double_exponential_smoothing(self):
        self.result = []
        self.Level = []
        self.Trend = []

        for i in range(len(self.series) + self.n_preds):
            if i == 0:  # инициализируем значения компонент
                self.result.append(self.series[0])
                level, trend = self.series[0], self.series[1] - self.series[0]
                self.Level.append(level)
                self.Trend.append(trend)
                continue
            if i >= len(self.series):  # прогнозируем
                m = i - len(self.series) + 1
                self.result.append(level + m * trend)
            else:
                self.result.append(level + trend)
                val = self.series[i]
                prev_level, level = level, self.alpha * val + (1 - self.alpha) * (
                    level + trend
                )
                trend = self.beta * (level - prev_level) + (1 - self.beta) * trend

            self.Level.append(level)
            self.Trend.append(trend)


class HoltWinters:

    """
    Модель Хольта-Винтерса тройного экспоненциального сглаживания с методом Брутлага для детектирования аномалий
    Про алгоритм подробнее здесь:
    https://habr.com/ru/company/ods/blog/327242/
    Про метод Брутлага подробнее здесь:
    https://fedcsis.org/proceedings/2012/pliks/118.pdf

    Parameters
    ----------
    series: исходный временной ряд
    slen: длина сезона
    alpha, beta, gamma: коэффициенты модели Хольта-Винтерса
    n_preds: горизонт предсказаний
    scaling_factor: задаёт ширину доверительного интервала по Брутлагу (обычно принимает значения от 2 до 3)

    Attributes
    ----------
    result: массив значений алгоритма тройного сглаживаня применненного к series
    Smooth: массив уровней (level) в модели сглаживаня
    Season: массив сезонных компонент в модели сглаживаня
    Trend: массив значений тренда в модели сглаживаня
    UpperBond: массив верхних границ дов.интервалов Брутлага
    LowerBond: массив нижних значений дов.интерваллов Брутлага

    """

    def __init__(self, series, slen, alpha, beta, gamma, n_preds, scaling_factor=1.96):
        self.series = series
        self.slen = slen
        self.alpha = alpha
        self.beta = beta
        self.gamma = gamma
        self.n_preds = n_preds
        self.scaling_factor = scaling_factor

    def initial_trend(self):
        sum = 0.0
        for i in range(self.slen):
            sum += float(self.series[i + self.slen] - self.series[i]) / self.slen
        return sum / self.slen

    def initial_seasonal_components(self):
        seasonals = {}
        season_averages = []
        n_seasons = int(len(self.series) / self.slen)
        # вычисляем сезонные средние
        for j in range(n_seasons):
            season_averages.append(
                sum(self.series[self.slen * j : self.slen * j + self.slen])
                / float(self.slen)
            )
        # вычисляем начальные значения
        for i in range(self.slen):
            sum_of_vals_over_avg = 0.0
            for j in range(n_seasons):
                sum_of_vals_over_avg += (
                    self.series[self.slen * j + i] - season_averages[j]
                )
            seasonals[i] = sum_of_vals_over_avg / n_seasons
        return seasonals

    def triple_exponential_smoothing(self):
        self.result = []
        self.Smooth = []
        self.Season = []
        self.Trend = []
        self.PredictedDeviation = []
        self.UpperBond = []
        self.LowerBond = []

        for i in range(len(self.series) + self.n_preds):
            if i == 0:  # инициализируем значения компонент
                smooth = self.series[0]
                trend = self.initial_trend()
                seasonals = self.initial_seasonal_components()
                deviations = np.array([0.0] * self.slen)
                self.result.append(self.series[0])
                self.Smooth.append(smooth)
                self.Trend.append(trend)

                self.Season.append(seasonals[i % self.slen])

                self.PredictedDeviation.append(deviations[i % self.slen])

                self.UpperBond.append(
                    self.result[0] + self.scaling_factor * self.PredictedDeviation[0]
                )

                self.LowerBond.append(
                    self.result[0] - self.scaling_factor * self.PredictedDeviation[0]
                )
                continue
            if i >= len(self.series):  # прогнозируем
                m = i - len(self.series) + 1
                self.result.append(smooth + m * trend + seasonals[i % self.slen])

                # во время прогноза с каждым шагом увеличиваем неопределенность
                prev_deviation = deviations[i % self.slen]
                deviations[i % self.slen] = deviations[i % self.slen] * 1.01

            else:
                self.result.append(smooth + trend + seasonals[i % self.slen])
                val = self.series[i]
                prev_smooth, smooth = smooth, self.alpha * (
                    val - seasonals[i % self.slen]
                ) + (1 - self.alpha) * (smooth + trend)
                trend = self.beta * (smooth - prev_smooth) + (1 - self.beta) * trend
                seasonals[i % self.slen] = (
                    self.gamma * (val - smooth)
                    + (1 - self.gamma) * seasonals[i % self.slen]
                )

                # Отклонение рассчитывается в соответствии с алгоритмом
                # Брутлага
                prev_deviation = deviations[i % self.slen]
                deviations[i % self.slen] = (
                    self.gamma * np.abs(self.series[i] - self.result[i])
                    + (1 - self.gamma) * prev_deviation
                )

            self.UpperBond.append(
                self.result[-1] + self.scaling_factor * prev_deviation
            )

            self.LowerBond.append(
                self.result[-1] - self.scaling_factor * prev_deviation
            )

            self.Smooth.append(smooth)
            self.Trend.append(trend)
            self.Season.append(seasonals[i % self.slen])
            self.PredictedDeviation.append(deviations[i % self.slen])


def timeseriesCVscore(x, data, r=0, method="HoltWinters", slen=7):
    """
    Производит кросс-валидацию на временных рядах для модели линейного тренда Хольта или модели Хольта-Винтерса
    Максимальное значение n_splits, таково, что (n_splits + 1) * 2 * slen <= len(data) (для линейной модели Хольта slen=1)
    Возвращает функцию, которую надо передать на вход оптимизатору, например:
    opt = scipy.optimize.minimize(timeseriesCVscore, x0=[0, 0, 0], args=(data, ), method="TNC", bounds = ((0, 1), (0, 1), (0, 1)))
    Из оптимизатора можно взять  оптимальные значение параметров:
    alpha, beta, gamma = opt.x

    Parameters
    ----------
    x: переменная, содержащая параметры модели (для Хольта: [alpha, beta], для Хольта-Винтерса: [alpha, beta, gamma])
    data: pd.Series - тренировочные данные для кросс-валидации
    r: коэффициент дисконтирования для взвешенной MSE, должен быть больше нуля
        По умолчанию = 0 - это эквивалентно обыкновенной MSE, а чем он больше, тем меньший вклад в ошибку дают более ранние значения
    method: Какую модель требуется валидировать двойного ('Holt') или тройного ('HoltWinters') экспоненциального сглаживания
    slen: Длина сезона для method = 'HoltWinters'
    """
    # Метрика
    def weighted_mse(actual, predictions, r):
        weights = [1 / np.power(1 + r, i) for i in range(len(actual), 0, -1)]
        return np.mean(
            ((np.array(actual) - np.array(predictions)) ** 2) * np.array(weights)
        )

    # Вектор ошибок
    errors = []

    # Данные в numpy массив
    values = data.values

    # Задаём число фолдов для кросс-валидации
    tscv = TimeSeriesSplit(n_splits=3)

    # Идем по фолдам, на каждом обучаем модель, строим прогноз на отложенной
    # выборке и считаем ошибку
    for train, test in tscv.split(values):

        if method == "HoltWinters":
            model = HoltWinters(
                series=values[train],
                slen=slen,
                alpha=x[0],
                beta=x[1],
                gamma=x[2],
                n_preds=len(test),
            )
            model.triple_exponential_smoothing()

        if method == "Holt":
            model = HoltLinearTrend(
                series=values[train], alpha=x[0], beta=x[1], n_preds=len(test)
            )
            model.double_exponential_smoothing()

        predictions = model.result[-len(test) :]
        actual = values[test]

        # Можно считать обыычный MSE или взвесить и дать больший вес свежим
        # значением
        error = weighted_mse(actual, predictions, r=r)
        errors.append(error)

    # Возвращаем средний квадрат ошибки по вектору ошибок
    return np.mean(np.array(errors))


def plotHolt(model, dataset, target, predict_interval, xlim=None):
    """
    Отрисовавает график временного ряда с наложением результата модели

    Parameters
    ----------
    model: обучення модель Хольта
    dataset: Объект pandas.DataFrame
    target: Пригнозирумая переменная
    predict_interval: Временной интервал для прогнозирования
    xlim: Сколько последних точек надо отобразить на графике, по умолчанию - все
    """
    if len(model.result) > len(dataset):
        dataset = pd.concat(
            [
                dataset,
                pd.DataFrame(np.array([np.NaN] * predict_interval), columns=[target]),
            ]
        )
    plt.figure(figsize=(25, 10))
    plt.plot(model.result, "b", label="Model")
    plt.plot(dataset[target].values, "g", label="Actual")
    plt.axvspan(
        len(dataset) - predict_interval - 1, len(dataset), alpha=0.5, color="lightgrey"
    )
    plt.grid(True)
    plt.axis("tight")
    plt.legend(loc="best", fontsize=13)
    if xlim:
        plt.xlim(len(dataset) - xlim, len(dataset))
    plt.show()


def plotHoltWinters(model, dataset, target, predict_interval, xlim=None):
    """
    Отрисовавает график временного ряда с наложением прогнозируемого ряда
    Отражает доверительный интревал Брутлага и аномальные относительно него значения

    Parameters
    ----------
    model: обучення модель Хольта-Винтреса
    dataset: Объект pandas.DataFrame
    target: Пригнозирумая переменная
    predict_interval: Временной интервал для прогнозирования
    xlim: Сколько последних точек надо отобразить на графике, по умолчанию - все
    """
    if len(model.result) > len(dataset):
        dataset = pd.concat(
            [
                dataset,
                pd.DataFrame(np.array([np.NaN] * predict_interval), columns=[target]),
            ]
        )
    Anomalies = np.array([np.NaN] * len(dataset[target]))
    Anomalies[dataset[target].values < model.LowerBond] = dataset[target].values[
        dataset[target].values < model.LowerBond
    ]
    Anomalies[dataset[target].values > model.UpperBond] = dataset[target].values[
        dataset[target].values > model.UpperBond
    ]
    plt.figure(figsize=(25, 10))
    plt.plot(model.result, "b", label="Model")
    plt.plot(model.UpperBond, "k--", alpha=0.5, label="Up/Low confidence")
    plt.plot(model.LowerBond, "k--", alpha=0.5)
    plt.fill_between(
        x=range(0, len(model.result)),
        y1=model.UpperBond,
        y2=model.LowerBond,
        alpha=0.5,
        color="grey",
    )
    plt.plot(dataset[target].values, "g", label="Actual")
    plt.plot(Anomalies, "ro", markersize=7, label="Anomalies")
    plt.axvspan(
        len(dataset) - predict_interval - 1, len(dataset), alpha=0.5, color="lightgrey"
    )
    plt.grid(True)
    plt.axis("tight")
    plt.legend(loc="best", fontsize=13)
    if xlim:
        plt.xlim(len(dataset) - xlim, len(dataset))
    plt.show()
