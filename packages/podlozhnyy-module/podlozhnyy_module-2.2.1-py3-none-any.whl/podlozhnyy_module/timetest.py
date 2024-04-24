from podlozhnyy_module import np, pd


def stat_difference_by_flg(
    df: pd.core.frame.DataFrame,
    feature: str,
    target: str,
    name: str,
    flg: str,
    num_buck: int = 10,
):
    """
    Считает разность в значениях целевой переменной между подмножествами исходного df, разбитого по флагу
    Подсчет происходит по бакетам признака feature если он числовой и просто по его значениям, если категориальный

    Parameters
    ----------
    df: Объект pandas.DataFrame
    feature: Название признака (числового или категориального)
    target: Название бинарной целевой переменной
    name: Как обозвать целевой признак
    flg: Название колонки-флага по которой исходный фрейм разбивается на две части. Вычитание из flg=0, как будто из прошлого
    num_buck: Количество бакетов, если признак числовой
    """
    if str(df[feature].dtype) in ("object", "category"):
        agg = (
            df.assign(obj_cnt=1)
            .rename(columns={feature: "bucket"})
            .groupby([flg, "bucket"], as_index=False)
            .agg({target: "mean", "obj_cnt": "sum"})
            .rename(columns={target: "AR", "obj_cnt": "feature_cnt"})
        )
        after = agg[agg[flg] == 1].copy()
        before = agg[agg[flg] == 0].copy()

        return (
            before.join(after.set_index("bucket"), on="bucket", rsuffix="_after")
            .assign(
                AR_decrease_mean=lambda x: x.AR - x.AR_after,
                AR_decrease_std=lambda x: np.sqrt(
                    (x.AR * (1 - x.AR) / x.feature_cnt)
                    + (x.AR_after * (1 - x.AR_after) / x.feature_cnt_after)
                ),
            )
            .assign(
                AR_decrease_min=lambda x: x.AR_decrease_mean - 1.96 * x.AR_decrease_std,
                AR_decrease_max=lambda x: x.AR_decrease_mean + 1.96 * x.AR_decrease_std,
            )
            .assign(
                AR_decrease_overall=lambda x: x.AR_decrease_mean
                * x.feature_cnt_after
                / after.feature_cnt.sum()
            )[
                [
                    "bucket",
                    "AR_decrease_overall",
                    "AR_decrease_mean",
                    "AR_decrease_min",
                    "AR_decrease_max",
                ]
            ]
            .sort_values(by="AR_decrease_overall", ascending=False)
            .rename(
                columns={
                    "AR_decrease_overall": name + "_decrease_overall",
                    "AR_decrease_mean": name + "_decrease_mean",
                    "AR_decrease_min": name + "_decrease_min",
                    "AR_decrease_max": name + "_decrease_max",
                }
            )
            .set_index("bucket")
        )

    else:
        # Бьем на бакеты, считаем AR до и после
        agg = (
            df[df[feature].notnull()]
            .assign(bucket=np.ceil(df[feature].rank(pct=True) * num_buck), obj_cnt=1)
            .groupby([flg, "bucket"], as_index=False)
            .agg({target: "mean", "obj_cnt": "sum", feature: "mean"})
            .rename(
                columns={target: "AR", "obj_cnt": "feature_cnt", feature: "feature_avg"}
            )
        )
        # Разделяем фрейм на до и после
        after = agg[agg[flg] == 1].copy()
        before = agg[agg[flg] == 0].copy()
        # Считаем среднюю разницу и доверительный интервал для этой средней
        return (
            before.join(after.set_index("bucket"), on="bucket", rsuffix="_after")
            .assign(
                AR_decrease_mean=lambda x: x.AR - x.AR_after,
                AR_decrease_std=lambda x: np.sqrt(
                    (x.AR * (1 - x.AR) / x.feature_cnt)
                    + (x.AR_after * (1 - x.AR_after) / x.feature_cnt_after)
                ),
            )
            .assign(
                AR_decrease_min=lambda x: x.AR_decrease_mean - 1.96 * x.AR_decrease_std,
                AR_decrease_max=lambda x: x.AR_decrease_mean + 1.96 * x.AR_decrease_std,
            )
            .assign(
                AR_decrease_overall=lambda x: x.AR_decrease_mean
                * x.feature_cnt_after
                / after.feature_cnt.sum()
            )[
                [
                    "bucket",
                    "feature_avg",
                    "feature_avg_after",
                    "AR_decrease_overall",
                    "AR_decrease_mean",
                    "AR_decrease_min",
                    "AR_decrease_max",
                ]
            ]
            .rename(columns={"feature_avg": "feature_avg_before"})
            .rename(
                columns={
                    "AR_decrease_overall": name + "_decrease_overall",
                    "AR_decrease_mean": name + "_decrease_mean",
                    "AR_decrease_min": name + "_decrease_min",
                    "AR_decrease_max": name + "_decrease_max",
                }
            )
            .set_index("bucket")
        )
