from scipy.stats import t as student
from scipy.stats import chi2_contingency as chi2

from podlozhnyy_module import np, pd, plt, sns


def plot_corr_matrix(
    df: pd.core.frame.DataFrame,
    features: list = None,
    diagram: str = "heat",
    clustering: str = "complete",
    **kwargs,
) -> None:
    """
    Строит матрицу корреляций признаков

    Parameters
    ----------
    df: Объект pandas.DataFrame
    features: Список признаков, взаимную корреляцию которых требуется посчитать, default=None
    diagram: Тип построенной диаграммы {'cluster', 'heat'}, , default='heat'
    clustering: Объект scipy.cluster.hierarchy.linkage() если `diagram` имеет значение 'cluster'
    
    **kwargs: Переменные для функции `correlation_significance`
    """
    corr = correlation_significance(df, features, **kwargs)
    plt.figure(figsize=(12, 12), facecolor="floralwhite")
    if diagram == "cluster":
        sns.clustermap(corr, method=clustering,  annot=True, cmap="RdBu", fmt=".2f")
    else:
        sns.heatmap(corr, vmax=1, square=True, annot=True, cmap="RdBu", fmt=".2f")
    plt.title("Correlation/significance between different features")
    bottom, top = plt.ylim()
    plt.ylim([bottom + 0.05, top - 0.05])
    plt.show()


def phi_cramer_coeff(contingency_table) -> float:
    """
    Возвращает коэффициент корреляции V-Крамера

    Parameters
    ----------
    contingency_table: Матрица сопряженности, например pd.crosstab(df[A], df[B])
    """
    chi_squared_stats = chi2(contingency_table.fillna(0))
    k1, k2 = contingency_table.shape
    n = contingency_table.sum().sum()
    return (chi_squared_stats[0] / (n * (min(k1, k2) - 1))) ** 0.5, chi_squared_stats[1]


def r2_significance(r2: float, n: int) -> float:
    """
    Расчет значимости корреляции методом Фишера

    Parameters
    ----------
    r2: Значение коэффициента R^2
    n: Размерность признаков
    """
    t = (r2 * (n - 2) ** 0.5) / max((1 - r2 ** 2) ** 0.5, 1e-3)
    return 2 * (1 - student.cdf(abs(t), df=n-2))


def correlation_significance(
    df: pd.core.frame.DataFrame,
    features: list = None,
    include: str="numerical",
    method: str = "pearson",
    pvalue: bool=False,
) -> pd.core.frame.DataFrame:
    """
    Возвращает матрицу значимости/коэффициентов корреляции признаков

    Parameters
    ----------
    df: Объект pandas.DataFrame
    features: Список названий признаков, если не указан - все признаки соответствующие параметру `include`, default=None
    include: Признаки какого типа принимать к рассмотрению {'numerical', 'categorical'}, default='numerical'
    method: Метод расчета корреляции в случае числовых признаков: {'pearson', 'kendall', 'spearman'}, default='pearson'
    pvalue: Если True возвращает значимость корреляции, иначе - коэффициенты, default=False
    """

    def select_columns(df, include):
        if include == "categorical":
            return df.select_dtypes(include=['object', 'category']).columns.to_list()
        elif include == "numerical":
            return df.select_dtypes(exclude=['object', 'category']).columns.to_list()
        else:
            raise ValueError("include must have either `numerical` or `categorical` value")

    if features is None:
        features = select_columns(df, include)
    else:
        features = select_columns(df[features], include)

    rows = []
    N = len(features)

    if include == "numerical":
        corr = df[features].corr(method=method)

    for i in range(N - 1):
        row = [None] * (i + 1)
        for j in range(i + 1, N):
            if include == "numerical":
                coef = corr.iloc[i, j]
                n = df[df[corr.index[i]].notnull() & df[corr.index[j]].notnull()].shape[0]
                p_val = r2_significance(coef, n)
            elif include == "categorical":
                contingency_table = pd.crosstab(df[features[i]], df[features[j]])
                coef, p_val = phi_cramer_coeff(contingency_table)
            if pvalue:
                row.append(p_val)
            else:
                row.append(coef)
        rows.append(row)
    rows.append([None] * N)
    data = (
        pd.DataFrame(rows, index=features, columns=features)
        .fillna(0)
        .apply(round, args=(3,))
    )
    return data + data.T + (np.zeros((N, N)) if pvalue else np.eye(N))
