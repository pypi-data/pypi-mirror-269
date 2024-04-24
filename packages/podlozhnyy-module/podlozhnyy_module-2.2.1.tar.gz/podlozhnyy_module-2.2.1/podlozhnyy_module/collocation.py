from itertools import combinations

from nltk.corpus import stopwords

from podlozhnyy_module import pd


def prepare_frequency_dictionary(
    documents: dict, length: int, analysed_documents: set
) -> dict:
    """
    Подготавливает словарь частотности коллокаций

    Parameters
    ----------
    documents: Словарь частот документов
    length: Длина выделяемой коллокации
    analysed_documents: Множество проанализированных ранее документов
    """
    frequency_dictionary = dict()
    for document, frequency in documents.items():
        unique_words = list(set(document))
        if document not in analysed_documents:
            for collocation in combinations(unique_words, length):
                frequency_dictionary[
                    collocation
                ] = frequency + frequency_dictionary.get(collocation, 0)
    return frequency_dictionary


def filter_frequency_dictionary(
    frequency_dictionary: dict,
    freq_filter: int,
    word_filter=None,
) -> None:
    """
    Фильтрует словарь частотности коллокаций на основе:
     - минимальной частотности
     - бинарной функции слов

    Parameters
    ----------
    frequency_dictionary: Словарь частотности коллокаций
    freq_filter: Минимальная частота коллокации
    word_filter: Функция от слова возвращающая True или False, default=None
    """
    matched_keys = set()
    for words, score in frequency_dictionary.items():
        if freq_filter and score < freq_filter:
            matched_keys.add(words)
        if word_filter and max([word_filter(word) for word in words]):
            matched_keys.add(words)
    for words in matched_keys:
        frequency_dictionary.pop(words)


def source_matching_dictionary(
    documents: dict,
    lengths: list,
    freq_filter=None,
    word_filter=None,
    verbose: bool = False,
) -> dict:
    """
    Возвращает словарь, соотносящий каждому документу самую популярную коллокацию, среди документов которым не была сопоставлена никакая более популярная коллокация

    Parameters
    ----------
    documents: Словарь частот документов
    lengths: Массив длин коллокаций, которые необходимо выделить в порядке приоритета
    freq_filter: Минимальная частота коллокации для учета, default=None
    freq_filter: Функция от слова возвращающая True или False, по умолчанию отбрасываются все коллокации со словами короче 3 букв и слова входящие в стоп лист английского языка, default=None
    verbose: Необходим ли подробный вывод работы программы, default=False
    """
    source_dictionary = dict()
    temp = pd.DataFrame(documents.items(), columns=["documents", "frequency"])
    if not word_filter:
        word_filter = lambda w: len(w) < 3 or w.lower() in set(
            stopwords.words("english")
        )
    for length in lengths:
        cnt = 0
        analysed_documents = set()
        frequency_dictionary = prepare_frequency_dictionary(
            documents, length, analysed_documents
        )
        filter_frequency_dictionary(frequency_dictionary, freq_filter, word_filter)
        while frequency_dictionary:
            scores = list(frequency_dictionary.items())
            scores.sort(key=lambda i: i[1], reverse=True)
            collocation, score = scores[0]
            docs = temp[
                temp.documents.apply(
                    lambda document: min([word in document for word in collocation])
                )
            ]
            number_of_docs = docs.shape[0]
            if number_of_docs > 1:
                if verbose:
                    print("\nCollocation:", collocation, flush=True)
                for document in docs.documents.values:
                    if not source_dictionary.get(document):
                        source_dictionary[document] = collocation
                        if verbose:
                            print(document, end=", ")
            for document in docs.documents.values:
                analysed_documents.add(document)
            if verbose:
                print("\nDocuments contained:", len(analysed_documents) - cnt)
            cnt = len(analysed_documents)
            frequency_dictionary = prepare_frequency_dictionary(
                documents, length, analysed_documents
            )
            filter_frequency_dictionary(frequency_dictionary, freq_filter, word_filter)
            if verbose:
                print("\n")
    return source_dictionary
