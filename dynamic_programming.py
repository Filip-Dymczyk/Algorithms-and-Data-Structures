import numpy as np


def recursive_matching(P: str, T: str, i: int, j: int) -> int:
    if i == 0:
        return len(T[:j])
    if j == 0:
        return len(P[:i])
    swap = recursive_matching(P, T, i - 1, j - 1) + (P[i] != T[j])
    insert = recursive_matching(P, T, i, j - 1) + 1
    delete = recursive_matching(P, T, i - 1, j) + 1

    return min(swap, insert, delete)


def PD_matching(P: str, T: str) -> int:
    D = np.zeros((len(P), len(T)))
    D[0] = np.array([i for i in range(len(T))])
    for i in range(len(P)):
        D[i, 0] = i
    for i in range(1, D.shape[0]):
        for j in range(1, D.shape[1]):
            swap = D[i - 1, j - 1] + (P[i] != T[j])
            insert = D[i, j - 1] + 1
            delete = D[i - 1, j] + 1
            min_cost = min(swap, insert, delete)
            D[i, j] = min_cost
    return int(D[len(P) - 1, len(T) - 1])


def PD_matching_with_path(P: str, T: str) -> str:
    D = np.zeros((len(P), len(T)))
    D[0] = np.array([i for i in range(len(T))])
    for i in range(len(P)):
        D[i, 0] = i
    parent = []
    for i in range(len(P)):
        parent.append(['X' for _ in range(len(T))])
    parent = np.array(parent)
    parent[0, 1:] = np.array(['I' for _ in range(1, len(T))])
    for i in range(1, len(P)):
        parent[i, 0] = 'D'
    for i in range(1, D.shape[0]):
        for j in range(1, D.shape[1]):
            swap = D[i - 1, j - 1] + (P[i] != T[j])
            insert = D[i, j - 1] + 1
            delete = D[i - 1, j] + 1
            min_cost = min(swap, insert, delete)
            D[i, j] = min_cost
            if min_cost == swap:
                if P[i] != T[j]:
                    parent[i, j] = 'S'
                else:
                    parent[i, j] = 'M'
            elif min_cost == insert:
                parent[i, j] = 'I'
            else:
                parent[i, j] = 'D'
    path = []
    i = len(P) - 1
    j = len(T) - 1
    while parent[i, j] != 'X':
        operation = parent[i, j]
        path.append(operation)
        if operation == 'M' or operation == 'S':
            i -= 1
            j -= 1
        elif operation == 'I':
            j -= 1
        elif operation == 'D':
            i -= 1
    path.reverse()
    return ''.join(path)


def sub_match(P: str, T: str) -> int:
    D = np.zeros((len(P), len(T)))
    for i in range(len(P)):
        D[i, 0] = i
    parent = []
    for i in range(len(P)):
        parent.append(['X' for _ in range(len(T))])
    parent = np.array(parent)
    for i in range(1, len(P)):
        parent[i, 0] = 'D'
    for i in range(1, D.shape[0]):
        for j in range(1, D.shape[1]):
            swap = D[i - 1, j - 1] + (P[i] != T[j])
            insert = D[i, j - 1] + 1
            delete = D[i - 1, j] + 1
            min_cost = min(swap, insert, delete)
            D[i, j] = min_cost
            if min_cost == swap:
                if P[i] != T[j]:
                    parent[i, j] = 'S'
                else:
                    parent[i, j] = 'M'
            elif min_cost == insert:
                parent[i, j] = 'I'
            else:
                parent[i, j] = 'D'
    i = len(P) - 1
    j = 0
    for k in range(1, len(T)):
        if D[i, k] < D[i, j]:
            j = k
    return j


def lcs(P: str, T: str) -> str:
    D = np.zeros((len(P), len(T)))
    D[0] = np.array([i for i in range(len(T))])
    for i in range(len(P)):
        D[i, 0] = i
    parent = []
    for i in range(len(P)):
        parent.append(['X' for _ in range(len(T))])
    parent = np.array(parent)
    parent[0, 1:] = np.array(['I' for _ in range(1, len(T))])
    for i in range(1, len(P)):
        parent[i, 0] = 'D'
    for i in range(1, D.shape[0]):
        for j in range(1, D.shape[1]):
            swap = D[i - 1, j - 1] + float('inf') if P[i] != T[j] else 0
            insert = D[i, j - 1] + 1
            delete = D[i - 1, j] + 1
            min_cost = min(swap, insert, delete)
            D[i, j] = min_cost
            if min_cost == swap:
                if P[i] != T[j]:
                    parent[i, j] = 'S'
                else:
                    parent[i, j] = 'M'
            elif min_cost == insert:
                parent[i, j] = 'I'
            else:
                parent[i, j] = 'D'
    res = ""
    i = len(P) - 1
    j = len(T) - 1
    while parent[i, j] != 'X':
        operation = parent[i, j]
        if operation == 'M':
            res += T[j]
            i -= 1
            j -= 1
        elif operation == 'I':
            j -= 1
        elif operation == 'D':
            i -= 1
    return res[::-1]


def main():
    P = ' kot'
    T = ' pies'
    min_cost = recursive_matching(P, T, len(P) - 1, len(T) - 1)
    print(f"Dla wyrazów - {P} i {T}, minimalny koszt to: {min_cost}")
    print('------------------------------------------------------------------------')
    P = ' biały autobus'
    T = ' czarny autokar'
    min_cost = PD_matching(P, T)
    print(f"Dla wyrazów - {P} i {T}, minimalny koszt to: {min_cost}")
    print('------------------------------------------------------------------------')
    P = ' thou shalt not'
    T = ' you should not'
    p = PD_matching_with_path(P, T)
    print(f'Ścieżka: {p}')
    print('------------------------------------------------------------------------')
    P = ' bin'
    T = ' mokeyssbanana'
    idx_start = sub_match(P, T)
    print(f"Indeks najlepszego dopasowania podciągu {P} w {T}: {idx_start - len(P.strip()) + 1}")
    print('------------------------------------------------------------------------')
    P = ' democrat'
    T = ' republican'
    LCS = lcs(P, T)
    print(f"Najdłuższa wspólna sekwencja dla {P} i {T}: {LCS}")
    print('------------------------------------------------------------------------')
    T = ' 243517698'
    T_new = T.strip()
    P = list(T_new)
    P = sorted(P, key=int)
    P = " " + ''.join(P)
    LMS = lcs(P, T)
    print(f"Najdłuższa podsekwencja monotoniczna dla {P} i {T}: {LMS}")
    print('------------------------------------------------------------------------')


if __name__ == '__main__':
    main()
