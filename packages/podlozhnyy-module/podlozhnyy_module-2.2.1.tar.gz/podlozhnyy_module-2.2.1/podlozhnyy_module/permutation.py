from itertools import combinations, product

from podlozhnyy_module import np


def permutation_t_stat(sample1, sample2):
    return np.mean(sample1) - np.mean(sample2)


def get_random_permutations(n, max_permutations):
    return set(
        [tuple(x) for x in 2 * np.random.randint(2, size=(max_permutations, n)) - 1]
    )


def permutation_zero_dist_one_samp(sample, mean, max_permutations):
    centered_sample = np.array(sample) - mean
    if max_permutations:
        signs_array = get_random_permutations(len(sample), max_permutations)
    else:
        signs_array = product([-1, 1], repeat=len(sample))
    return [np.mean(centered_sample * signs) for signs in signs_array]


def get_random_combinations(n1, n2, max_combinations):
    index = list(range(n1 + n2))
    indices = set([tuple(index)])
    for i in range(max_combinations - 1):
        np.random.shuffle(index)
        indices.add(tuple(index))
    return [(index[:n1], index[n1:]) for index in indices]


def permutation_zero_dist_ind(sample1, sample2, max_combinations):
    joined_sample = np.hstack((sample1, sample2))
    n1, n2 = len(sample1), len(sample2)
    n = len(joined_sample)
    if max_combinations:
        indices = get_random_combinations(n1, n2, max_combinations)
    else:
        indices = [
            (list(index), filter(lambda i: i not in index, range(n)))
            for index in combinations(range(n), n1)
        ]
    return [
        joined_sample[list(i[0])].mean() - joined_sample[list(i[1])].mean()
        for i in indices
    ]


def permutation_test(
    test,
    control,
    kind: str = "independent",
    max_permutations: int = None,
    alternative: str = "two-sided",
):
    """
    Проводит одно- или двух- выборочный статистический тест, используя семейство перестановочных критериев
    Возвращает значение p-value для заданного типа альтернативы

    Parameters
    ----------
    test: list
        Тестовая выборка
    control: list, float or integer
        Контрольная выборка или число в случае одновыборочного теста
    kind: str
        Связаны ли выборки в двухстороннем тесте {'related', 'independent'}, default='independent'
    max_permutations: int
        Максимальное количество перестановок, исключительно полезно в случае больших выборок, default=None
    alternative: str
        Тип альтернативы: {'two-sided', 'less', 'greater'}, default='two-sided'
    """
    if alternative not in ("two-sided", "less", "greater"):
        raise ValueError(
            "alternative not recognized, should be 'two-sided', 'less' or 'greater'"
        )

    if kind not in ("independent", "related"):
        raise ValueError("kind not recognized, should be 'related' or 'independent'")

    if isinstance(control, int) or isinstance(control, float):
        zero_distr = permutation_zero_dist_one_samp(test, control, max_permutations)
    elif kind == "related":
        if len(test) != len(control):
            raise ValueError("related samples must have the same size")
        zero_distr = permutation_zero_dist_one_samp(
            np.array(test) - np.array(control), 0.0, max_permutations
        )
    else:
        zero_distr = permutation_zero_dist_ind(test, control, max_permutations)

    t_stat = permutation_t_stat(test, control)

    if alternative == "two-sided":
        return sum([1.0 if abs(x) >= abs(t_stat) else 0.0 for x in zero_distr]) / len(
            zero_distr
        )

    if alternative == "less":
        return sum([1.0 if x <= t_stat else 0.0 for x in zero_distr]) / len(zero_distr)

    if alternative == "greater":
        return sum([1.0 if x >= t_stat else 0.0 for x in zero_distr]) / len(zero_distr)
