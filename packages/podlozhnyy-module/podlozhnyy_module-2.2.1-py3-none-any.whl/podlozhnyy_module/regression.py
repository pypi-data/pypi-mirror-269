from functools import wraps
from itertools import product
from math import log

import holoviews as hv
from scipy.stats import f as fisher
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
from sklearn.model_selection import train_test_split
from statsmodels.stats.proportion import proportion_confint

from podlozhnyy_module import np, pd, plt


def _set_options(func):
    """Обертка для применения визуальных настроек"""

    @wraps(func)
    def wrapper(*args, **kwargs):
        diagramm = func(*args, **kwargs)
        for bnd, opts in [("matplotlib", matplotlib_opts), ("bokeh", bokeh_opts)]:
            if bnd in hv.Store._options and bnd == hv.Store.current_backend:
                return diagramm.opts(opts)
        return diagramm

    return wrapper


colors = hv.Cycle(
    [
        "#1f77b4",
        "#ff7f0e",
        "#2ca02c",
        "#d62728",
        "#9467bd",
        "#8c564b",
        "#e377c2",
        "#7f7f7f",
        "#bcbd22",
        "#17becf",
    ]
)

matplotlib_opts = {
    "Scatter.Weight_of_Evidence": {
        "plot": dict(show_grid=True, legend_position="right", width=450),
        "style": dict(color="r", size=5),
    },
    "NdOverlay.Objects_rate": {
        "plot": dict(xrotation=45, legend_cols=1, legend_position="right"),
    },
    "Spread.Objects_rate": {
        "plot": dict(show_legend=True, show_grid=True),
        "style": dict(facecolor=colors),
    },
    "Overlay.Woe_Stab": {
        "plot": dict(legend_position="right"),
    },
    "Curve.Weight_of_Evidence": {
        "style": dict(color=colors),
    },
    "Spread.Confident_Intervals": {
        "plot": dict(show_grid=True, xrotation=45),
        "style": dict(facecolor=colors, alpha=0.3),
    },
}

bokeh_opts = {
    "Scatter.Weight_of_Evidence": {
        "plot": dict(
            show_grid=True, tools=["hover"], legend_position="right", width=450
        ),
        "style": dict(color="r", size=5),
    },
    "NdOverlay.Objects_rate": {
        "plot": dict(xrotation=45, legend_position="right", width=450),
    },
    "Spread.Objects_rate": {
        "plot": dict(show_legend=True, show_grid=True, tools=["hover"]),
        "style": dict(color=colors),
    },
    "Overlay.Woe_Stab": {
        "plot": dict(legend_position="right", width=450),
    },
    "Curve.Weight_of_Evidence": {
        "plot": dict(tools=["hover"]),
        "style": dict(color=colors),
    },
    "Spread.Confident_Intervals": {
        "plot": dict(show_grid=True, xrotation=45),
        "style": dict(color=colors, alpha=0.3),
    },
}


def make_bucket(df, feature, num_buck=10):
    """
    Производит разбиение на бакеты

    Parameters
    ----------
    df: Объект pandas.DataFrame
    feature: Название признака числового или категориального
    num_buck: Количество бакетов для группирровки
    """
    bucket = np.ceil(df[feature].rank(pct=True) * num_buck).fillna(num_buck + 1)
    agg = df[feature].groupby(bucket).agg(["min", "max"])

    def _format_buck(row):
        if row["bucket"] == num_buck + 1:
            return "missing"
        elif row["min"] == row["max"]:
            return _format_(row["min"])
        else:
            return _format_(row["min"]) + " - " + _format_(row["max"])

    bucket = (
        df[[feature]]
        .assign(bucket=bucket)
        .join(agg, on="bucket")
        .apply(_format_buck, axis=1)
    )

    return df.assign(bucket=bucket)


def _format_(x, decimal=3):
    """
    Форматируем названия бакетов

    Parameters
    ----------
    x: Вход - строка или число
    decimal: Желаемое кол-во знаков после запятой
    """
    if not isinstance(x, str):
        div, mod = x // 1, x % 1
        if mod == 0:
            if div == 0:
                return "%d" % x
            elif int(np.floor(np.log10(abs(div)))) < 3:
                return "%d" % x
        if div == 0:
            power = int(np.floor(np.log10(abs(mod))))
            digits = decimal - power - 1
            return "%s" % np.around(x, digits)
        else:
            power = int(np.floor(np.log10(abs(div))))
            digits = decimal
            if power < 3:
                return "%s" % np.around(x, digits)
            elif power < 10:
                return "%se+0%s" % (np.around(x / np.power(10, power), digits), power)
            else:
                return "%se+%s" % (np.around(x / np.power(10, power), digits), power)
    return "%s" % x


@_set_options
def check_linearity(df, feature, target, num_buck=10):
    """
    Позволяет оценивать линейность зависимости целевой переменной от признака.
    Строит график зависимости и лучшую регрессионную прямую (с наименьшим r_2)

    Parameters
    ----------
    df: Объект pandas.DataFrame
    feature: Название признака (числового!)
    target: Название целевой переменной
    num_buck: Количество бакетов, если признак числовой
    """
    return (
        df.pipe(make_bucket, feature, num_buck)
        .groupby("bucket")
        .mean()
        .pipe(
            lambda x: hv.Scatter(
                zip(np.array(x[feature]), np.array(x[target])),
                kdims=f"{feature}",
                vdims=f"{target}",
                label=f"Проверка линейности зависимости {target} от {feature}",
            )
            * simple_reg(np.array(x[feature]), np.array(x[target]))
        )
    )


@_set_options
def check_homoscedacity(df, feature, target):
    """
    Позволяет оценивать гомоскедастичность зависимости целевой переменной от признака.

    Parameters
    ----------
    df: Объект pandas.DataFrame
    feature: Название признака (числового!)
    target: Название целевой переменной
    """
    simple_model = LinearRegression()
    simple_model.fit(np.array(df[feature]).reshape(-1, 1), np.array(df[target]))
    predicts = simple_model.predict(np.array(df[feature]).reshape(-1, 1))

    def get_residuals(y, pred):
        return np.array(y) - np.array(pred)

    return hv.Scatter(
        zip(predicts, get_residuals(df[target], predicts)),
        kdims=["Estimated target"],
        vdims=["Residual"],
        label=f"Проверка гомоскедастичности признака {feature}",
    )


def _logit(p):
    """
    Возвращает логит от вероятности

    Parameters
    ----------
    p: вероятность просрочки
    """
    return np.log(p / (1 - p))


def _woe(p, q):
    """
    Считает WoE для бакета

    Parameters
    ----------
    p: вероятность просрочки в бакете
    q: вероятность просрочки на всем корпусе
    """
    p, q = np.clip([p, q], 0.001, 0.999)
    return _logit(p) - _logit(q)


def _woe_confint(n, cnt, q):
    """
    Считает 95%% доверительный интервал для WoE

    Parameters
    ----------
    n: кол-во просрочек в бакете
    cnt: кол-во элементов в бакете
    q: вероятность просрочки на всем корпусе
    """
    p_low, p_high = proportion_confint(n, cnt, method="normal")
    return _woe(p_low, q), _woe(p_high, q)


def bad_rate(df, feature, target, num_buck=10):
    """
    Считает bad_rate для каждого бакета признака в модели классификации.
    Возвращает датафрейм с аггрегациями (сумма таргета в бакете, среднее значение предсказания,
    количество эл-ов в бакете, среднее значение признака в бакете)
    Во избежание исключений наложено ограничение: 0.001 <= bad_rate <= 0.999

    Parameters
    ----------
    df: Объект pandas.DataFrame
    feature: Название признака (числового или категориального)
    target: Название целевой переменной
    num_buck: Количество бакетов, если признак числовой
    """
    if df[feature].dtype == "O":
        return (
            df.pipe(make_bucket, feature, num_buck)
            .assign(obj_cnt=1)
            .groupby("bucket")
            .agg({target: "sum", "obj_cnt": "sum"})
            .rename(columns={target: "target_sum"})
            .assign(bad_rate=lambda x: x.target_sum / x.obj_cnt)
        )
    else:
        return (
            df.pipe(make_bucket, feature, num_buck)
            .assign(obj_cnt=1)
            .groupby("bucket")
            .agg({target: "sum", "obj_cnt": "sum", feature: "mean"})
            .rename(columns={target: "target_sum", feature: "feature_avg"})
            .assign(bad_rate=lambda x: x.target_sum / x.obj_cnt)
        )


def woe(df, feature, target, num_buck=10):
    """
    Считает WOE для признака в модели классификации.
    Доля объектов каждого класса ограничивается 0.001 - снизу и 0.999 - сверху.

    Parameters
    ----------
    df: Объект pandas.DataFrame
    feature: Название признака (числового или категориального)
    target: Название целевой переменной
    num_buck: Количество бакетов, если признак числовой
    """
    agg = bad_rate(df, feature, target, num_buck).reset_index()
    agg = agg[agg.target_sum != 0]
    return (
        agg.assign(nums=agg["obj_cnt"].sum(), bad_nums=agg["target_sum"].sum())
        .assign(woe=lambda x: _woe(x.bad_rate, x.bad_nums / x.nums))
        .drop(["bad_nums", "nums"], axis=1)
        .sort_values(by="woe", ascending=False)
        .set_index("bucket")
    )


def IV(df, feature, target, num_buck=10):
    """
    Считает Information Value для признака в модели бинарной классификации.

    Parameters
    ----------
    df: Объект pandas.DataFrame
    feature: Название признака (числового или категориального)
    target: Название целевой переменной
    num_buck: Количество бакетов, если признак числовой
    """
    return (
        woe(df, feature, target, num_buck)
        .assign(
            iv=lambda x: (
                x.target_sum / x.target_sum.sum()
                - (x.obj_cnt - x.target_sum) / (x.obj_cnt.sum() - x.target_sum.sum())
            )
            * x.woe
        )
        .iv.sum()
    )


def iv_report(df, features, target, num_buck=10):
    """
    Считает IV для указанных признаков в модели классификации.
    Возвращает в порядке убывания кортежи из трех элементов:(признак, IV, интерпретация)

    Parameters
    ----------
    df: Объект pandas.DataFrame
    features: Список названий признаков (числовых или категориальных)
    target: Название целевой переменной
    num_buck: Количество бакетов для разбиения
    """

    def desc(x):
        if x > 0.5:
            power = "Suspicious"
        elif x > 0.3:
            power = "Strong"
        elif x > 0.1:
            power = "Medium"
        elif x > 0.02:
            power = "Weak"
        else:
            power = "Useless"
        return (x, power)

    ivs = {}
    for column in list(features):
        ivs[column] = desc(IV(df, column, target, num_buck))

    ivs = list(ivs.items())
    ivs.sort(key=lambda i: i[1], reverse=True)
    print("         Name         ||  Value  || Interpretation")
    print("--------------------------------------------------")
    for feature in ivs:
        print(f"{feature[0]:21} ||  {feature[1][0]:.3f}  || {feature[1][1]}")


def iv_agg(df, features, target, num_bucks=[10, 10]):
    """
    Считает совокупный IV для указанных признаков в модели бинарной классификации.

    Parameters
    ----------
    df: Объект pandas.DataFrame
    features: Список названий признаков (числовых или категориальных)
    target: Название целевой переменной
    num_bucks: Список количества бакетов для каждой из переменных
    """
    index = make_bucket(df[[features[-1]]], features[-1], num_buck=num_bucks[-1])[
        "bucket"
    ].values
    columns = []

    for i, feature in enumerate(features[:-1]):
        columns.append(
            make_bucket(df[[feature]], feature, num_buck=num_bucks[i])["bucket"].values
        )

    obj_cnt = pd.crosstab(index=index, columns=columns, margins=True)
    target_sum = pd.crosstab(
        index=index,
        columns=columns,
        values=df[target].values,
        aggfunc=np.sum,
        margins=True,
    )
    bad_rate = pd.crosstab(
        index=index,
        columns=columns,
        values=df[target].values,
        aggfunc=np.mean,
        margins=True,
    )
    agg = pd.DataFrame(
        {
            "obj_cnt": obj_cnt.iloc[:-1, :-1].unstack().values,
            "target_sum": target_sum.iloc[:-1, :-1].unstack().values,
            "bad_rate": bad_rate.iloc[:-1, :-1].unstack().values,
        }
    )
    agg = agg[agg.target_sum != 0]
    return (
        agg.assign(nums=agg["obj_cnt"].sum(), bad_nums=agg["target_sum"].sum())
        .assign(woe=lambda x: _woe(x.bad_rate, x.bad_nums / x.nums))
        .assign(
            iv=lambda x: (
                x.target_sum / x.target_sum.sum()
                - (x.obj_cnt - x.target_sum) / (x.obj_cnt.sum() - x.target_sum.sum())
            )
            * x.woe
        )
        .iv.sum()
    )


@_set_options
def simple_reg(predictor, target):
    """
    Строит простую линейную регрессию
    Использует для отрисовки прямой и подсчета r^2

    Parameters
    ----------
    predictor: Массив значений признака
    target: Массив значений целевой переменной
    """
    check = LinearRegression()
    check.fit(predictor.reshape(-1, 1), target)
    return hv.Curve(
        (
            np.array([min(predictor) - 1, max(predictor) + 1]),
            check.coef_ * np.array([min(predictor) - 1, max(predictor) + 1])
            + check.intercept_,
        )
    )


def r_2check(df, feature, target, num_buck=10):
    """
    Для заданного признака строт простую линейную регрессию для бакетов получаемых из функции woe
    Возвращает r2_score полученного результата

    Parameters
    ----------
    df: Объект pandas.DataFrame
    feature: Название признака (числового!)
    target: Название целевой переменной
    num_buck: Количество бакетов, если признак числовой
    """
    model = LinearRegression()
    data = woe(df, feature, target, num_buck)
    data = data[data.feature_avg.notnull()]
    X = np.array(data.feature_avg)
    y = np.array(data.woe)
    model.fit(X.reshape(-1, 1), y)
    return round(r2_score(y, model.predict(X.reshape(-1, 1))), 3)


@_set_options
def plot_woe_curve(df, feature, target, num_buck=10):
    """
    Считает WOE, и по полученным точкам строит лучшую прямую (с наибольшим r_2)
    Можно задавать размер изображения, например так:
        %%output size = 150

    Parameters
    ----------
    df: Объект pandas.DataFrame
    feature: Название признака (числового!)
    target: Название целевой переменной
    num_buck: Количество бакетов, если признак числовой
    """

    agg = bad_rate(df, feature, target, num_buck).reset_index()
    agg = agg[(agg.target_sum != 0) & (agg.feature_avg.notnull())]
    agg = (
        agg.assign(nums=agg["obj_cnt"].sum(), bad_nums=agg["target_sum"].sum())
        .assign(
            woe=lambda x: _woe(x.bad_rate, x.bad_nums / x.nums),
            woe_low=lambda x: _woe_confint(
                x.target_sum, x.obj_cnt, x.bad_nums / x.nums
            )[0],
            woe_high=lambda x: _woe_confint(
                x.target_sum, x.obj_cnt, x.bad_nums / x.nums
            )[1],
        )
        .assign(woe_u=lambda x: x.woe_high - x.woe, woe_b=lambda x: x.woe - x.woe_low)
    )

    r2_woe = r_2check(df, feature, target, num_buck)
    scatter = hv.Scatter(
        data=agg,
        kdims=["feature_avg"],
        vdims=["woe"],
        group="Weight of Evidence",
        label=f"r2_score = {r2_woe}",
    )
    errors = hv.ErrorBars(
        data=agg,
        kdims=["feature_avg"],
        vdims=["woe", "woe_u", "woe_b"],
        group="Confident Intervals",
    )
    reg = simple_reg(np.array(agg.feature_avg), np.array(agg.woe))
    return hv.Overlay(
        items=[scatter, errors, reg], group="Woe Curve", label=feature
    ).redim.range(
        feature_avg=(agg.feature_avg.min() * 1.15, agg.feature_avg.max() * 1.15),
        woe=(agg.woe.min() * 1.15, agg.woe.max() * 1.15),
    )


# Динамика переменных и WoE


@_set_options
def distribution(df, feature, date, num_buck=10, date_freq="Q"):
    """
    Строит график распределения признака во времени

    Parameters
    ----------
    df: Объект pandas.DataFrame
    feature: Название признака числового или категориального
    date: Наименование временной переменной
    num_buck: Количество бакетов, если признак числовой
    date_freq: Частота агрегации времени
    """
    agg = (
        df.pipe(make_bucket, feature, num_buck)
        .assign(obj_cnt=1)
        .groupby([pd.Grouper(key=date, freq=date_freq), "bucket"])
        .agg({"obj_cnt": sum})
        .reset_index()
        .assign(
            obj_total=lambda x: (
                x.groupby([pd.Grouper(key=date, freq=date_freq)])["obj_cnt"].transform(
                    "sum"
                )
            )
        )
        .assign(obj_rate=lambda x: x.obj_cnt / x.obj_total)
        .reset_index()
        .assign(
            objects_rate=lambda x: x.groupby(date)
            .apply(lambda y: y.obj_rate.cumsum().to_frame())
            .reset_index(drop=True)
        )
        .assign(obj_rate_u=0, obj_rate_b=lambda x: x["obj_rate"])
    )

    data = hv.Dataset(
        agg, kdims=["bucket", date], vdims=["objects_rate", "obj_rate_b", "obj_rate_u"]
    )

    return data.to.spread(
        kdims=[date],
        vdims=["objects_rate", "obj_rate_b", "obj_rate_u"],
        group="Objects rate",
        label=feature,
    ).overlay("bucket")


@_set_options
def woe_stab(df, feature, target, date, num_buck=3, date_freq="Q"):
    """
    Строит WoE признака во времени, позволяет оценить его устойчивость

    Parameters
    ----------
    df: Объект pandas.DataFrame
    feature: Название признака числового или категориального
    target: Название целевой переменной
    date: Наименование временной переменной
    num_buck: Количество бакетов, если признак числовой
    date_freq: Частота агрегации времени
    """
    agg = (
        df.pipe(make_bucket, feature, num_buck)
        .assign(obj_cnt=1)
        .groupby([pd.Grouper(key=date, freq=date_freq), "bucket"])
        .agg({target: "sum", "obj_cnt": sum})
        .rename(columns={target: "target_sum"})
        .assign(bad_rate=lambda x: x.target_sum / x.obj_cnt)
    )

    agg = (
        agg.assign(
            nums=agg.groupby([date])["obj_cnt"].transform("sum"),
            bad_nums=agg.groupby([date])["target_sum"].transform("sum"),
        )
        .assign(
            woe=lambda x: _woe(x.bad_rate, x.bad_nums / x.nums),
            woe_low=lambda x: _woe_confint(
                x.target_sum, x.obj_cnt, x.bad_nums / x.nums
            )[0],
            woe_high=lambda x: _woe_confint(
                x.target_sum, x.obj_cnt, x.bad_nums / x.nums
            )[1],
        )
        .assign(woe_u=lambda x: x.woe_high - x.woe, woe_b=lambda x: x.woe - x.woe_low)
        .reset_index()
    )

    agg = agg[agg.target_sum != 0]

    data = hv.Dataset(agg, kdims=["bucket", date], vdims=["woe", "woe_b", "woe_u"])

    confident_intervals = data.to.spread(
        kdims=[date], vdims=["woe", "woe_b", "woe_u"], group="Confident Intervals"
    ).overlay("bucket")
    woe_curves = data.to.curve(
        kdims=[date], vdims=["woe"], group="Weight of Evidence"
    ).overlay("bucket")
    return hv.Overlay(
        items=[confident_intervals * woe_curves], group="Woe Stab", label=f"{feature}"
    )


def HL(target, predict, num_buck=10):
    """
    Считает статистику Хосмера-Лемешева

    Parameters
    ----------
    target - истинные значения целевой переменной
    predict - предсказания вероятности
    num_buck - количество бакетов
    """
    data = pd.DataFrame({"target": target, "predict": predict})

    data = (
        data.pipe(make_bucket, "predict", num_buck)
        .assign(obj_cnt=1)
        .groupby("bucket")
        .agg({"target": "sum", "predict": "mean", "obj_cnt": "sum"})
        .assign(bad_rate=lambda x: x.target / x.obj_cnt)
        .reset_index()
    )
    return int(
        sum(
            (data.predict - data.bad_rate) ** 2
            / (data.predict * (1 - data.predict))
            * data.obj_cnt
        )
    )


@_set_options
def plot_gain_chart(target, predict, num_buck=10):
    """
    Строит gain_chart по истиным и предсказанным меткам
    На первом шаге бьет наблюдения на бакеты, затем считает средний bad_rate.
    На втором шаге строится график, где кривая обозначает предсказанное значение целевой переменной, столбцы - истинные.

    Parameters
    ----------
    target - истинные значения целевой переменной
    predict - предсказания вероятности
    num_buck - количество бакетов
    """
    data = pd.DataFrame({"target": target, "predict": predict})
    H = HL(target, predict, num_buck)
    data = (
        data.assign(bucket=np.ceil(data["predict"].rank(pct=True) * num_buck))
        .assign(obj_cnt=1)
        .groupby("bucket")
        .agg({"target": "sum", "predict": "mean", "obj_cnt": "sum"})
        .assign(bad_rate=lambda x: x.target / x.obj_cnt)
        .reset_index()
    )

    bars_gain = hv.Bars(
        data, kdims=["bucket"], vdims=["bad_rate"], label="observed"
    ).opts(plot={"xrotation": 90, "show_legend": True}, style={"color": "yellow"})

    curve_gain = hv.Curve(
        data, kdims=["bucket"], vdims=["predict"], label="predicted"
    ).opts(plot={"xrotation": 90, "show_legend": True}, style={"color": "black"})

    return (
        hv.Overlay([bars_gain, curve_gain])
        .redim.label(**{"target": "Bad Rate"})
        .relabel(f"HL_score = {H}")
        .opts(plot={"legend_position": "top_left"})
    )


def feature_importance(names, values, verbose=False, thr=0.05):
    """
    Возвращает словарь и печатает в порядке убывания коэффициенты для признаков

    Parameters
    ----------
    names: Список наименований признаков
    values: Список коэффициентов для этих признаков
    verbose: Стоит ли печатать результат
    thr: Не выводить признаки с меньшим вкладом
    """
    names = names.tolist()
    val_dict = {}
    for name, value in zip(names, values):
        val_dict[name] = round(value, 3)
    if verbose:
        coef_list = list(val_dict.items())
        coef_list.sort(key=lambda i: i[1], reverse=True)
        for i in coef_list:
            if i[1] >= thr:
                print(i[0], ":", round(i[1], 5))
    return val_dict


@_set_options
def plot_confusion_matrix(
    cm, classes, normalize=False, title="Confusion matrix", cmap=plt.cm.Blues
) -> None:
    """
    Печатает и отрисовывает матрицу ошибок для задачи классификации
    Для нормализации небходимо передать аргумент normalize=True

    Parameters
    ----------
    cm: Матрица ошибок вида metrics.confusion_matrix(.., ..)
    classes: Наименование для значений целевой переменной
    normalize: Булева переменная, для нормализации матрицы
    title: Название для графика
    cmap: Цветовая палитра, по умолчанию: plt.cm.Blues
    """
    plt.imshow(cm, interpolation="nearest", cmap=cmap)
    plt.title(title)
    plt.colorbar()
    tick_marks = np.arange(len(classes))
    bottom, top = plt.ylim()
    plt.xticks(tick_marks, classes, rotation=45)
    plt.yticks(tick_marks, classes, rotation=45)
    plt.ylim([bottom, top])

    if normalize:
        cm = cm.astype("float") / cm.sum(axis=1)[:, np.newaxis]
        print("Normalized confusion matrix")
    else:
        print("Confusion matrix, without normalization")

    print(cm)

    thresh = cm.max() / 2.0
    for i, j in product(range(cm.shape[0]), range(cm.shape[1])):
        plt.text(
            j,
            i,
            cm[i, j],
            horizontalalignment="center",
            verticalalignment="center",
            color="white" if cm[i, j] > thresh else "black",
        )

    plt.tight_layout()
    plt.ylabel("Истинный класс")
    plt.xlabel("Предсказанный класс")
    plt.show()


def regression_report(
    X: pd.core.frame.DataFrame, y: np.ndarray, model: object, **kwargs
) -> dict:
    """
    Обучает заданную модель регрессии на предоставленных данных.
    В стандартный поток вывода публикуются метрики качества построенной модели и важность признаков.
    Возвращает словарь весов признаков для линейной модели или словарь важности для деревьев и ансамблей.

    Parameters
    ----------
    X: Матрица признаков, объект pandas.DataFrame
    y: Целевая переменная (numpy массив или pandas.core.series.Series)

    Other Parameters
    ----------------
    **kwargs : переменные метода `feature_importance`
    """
    X_train, X_test, y_train, y_test = train_test_split(
        pd.get_dummies(
            X[::-1],
            prefix_sep="/",
            dummy_na=False,
            drop_first=False,
        ),
        y[::-1],
        test_size=0.2,
        shuffle=True,
    )
    model.fit(X_train, y_train)
    train_predict, test_predict = model.predict(X_train), model.predict(X_test)

    def r2_score(y_true, y_pred):
        rss = sum((y_true - y_pred) ** 2) / len(y_true)
        tss = y_true.var(ddof=0)
        r2 = 1 - rss / tss
        return r2

    def regression_significance(r2_score: float, n_objects: int, n_features: int):
        r, n, k = r2_score, n_objects, n_features
        f = (r**2 / k) / max(((1 - r**2) / (n - k - 1)), 1e-3)
        return 1 - fisher.cdf(f, dfn=k, dfd=n - k - 1)

    r2_train, r2_test = r2_score(y_train, train_predict), r2_score(y_test, test_predict)

    # Features number before get_dummies transformation
    p_value = regression_significance(r2_train, X_train.shape[0], X.shape[1])

    print(
        f"r2_test = {round(r2_test, 3)} (r2_train = {round(r2_train, 3)}, p_value = {round(p_value, 3)})\n"
    )

    try:
        type_name = str(type(model))
        if "linear_model" in type_name:
            if "logistic" in type_name:
                values = model.coef_[1]
            else:
                values = model.coef_
        else:
            values = model.feature_importances_
    except Exception as e:
        return e

    dictionary = feature_importance(names=X_train.columns, values=values, **kwargs)
    return dictionary
