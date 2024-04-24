from podlozhnyy_module import np, pd, plt, sns

sns.set_style(rc={"figure.facecolor": "floralwhite"})


def plot_hist(
    df: pd.core.frame.DataFrame, feature: str, target: str, n: int = 10
) -> None:
    """
    Строит приятную гистограмму распределения признака от целевой переменной

    Parameters
    ----------
    df: Объект pandas.DataFrame
    feature: Признак, распределение которого, требуется посмотреть
    target: Целевая переменная для разбиения признака
    n: Кол-во bin-ов, default=10
    """
    df2 = pd.melt(
        df[[feature, target]], id_vars=target, value_vars=[feature], value_name="target"
    )
    bins = np.linspace(df2["target"].min(), df2["target"].max(), n + 1)

    g = sns.FacetGrid(
        df2, col="variable", hue=target, palette="rainbow", col_wrap=2, height=10
    )
    g.map(plt.hist, "target", alpha=0.5, density=True, bins=bins, ec="k")
    g.axes[-1].legend()
    plt.show()


def plot_stacked_hist(df: pd.core.frame.DataFrame, feature: str, target: str) -> None:
    """
    Возвращает столбец распределения признака в рамках каждого из значений целевой переменной

    Parameters
    ----------
    df: Объект pandas.DataFrame
    feature: Признак, распределение которго, требуется посмотреть
    target: Целевая переменная, будет на оси x графика
    """
    overview = pd.crosstab(df[target], df[feature]).sort_values(target, ascending=True)
    sum_series = overview.sum(axis=1)
    for col in list(overview.columns):
        overview[col] = overview[col] / sum_series
    overview.plot(kind="bar", stacked=True)


def plot_dual_axis(
    data: pd.core.frame.DataFrame, col1: str, col2: str, title: str = None
):
    """
    Построение графика с двумя осями ординат

    Parameters
    ----------
    data: Объект pandas.DataFrame
    col1: Название основоного признака (левая ось)
    col2: Название дополнительного признака (правая ось)
    title: Заголовок графика
    """
    fig, ax1 = plt.subplots(figsize=(12, 6))
    ax2 = ax1.twinx()

    ax2.bar(data.index, data[col2], alpha=0.15, fill=True, edgecolor="b")
    ax1.plot(data.index, data[col1], "go--", linewidth=2)

    def naming(name):
        return " ".join([x[0].upper() + x[1:] for x in name.split("_")])

    if data.index.name:
        ax1.set_xlabel(naming(data.index.name))
    ax1.set_ylabel(naming(col1), color="g")
    ax2.set_ylabel(naming(col2), color="b")
    plt.title(title)
    plt.show()
