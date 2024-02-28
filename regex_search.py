import time
from typing import List
import os


def regex_naive(path: str, W: str) -> None:
    t_start = time.perf_counter()
    with open(path, encoding='utf-8') as f:
        text = f.readlines()
    S = ' '.join(text).lower()
    res = 0
    if len(S) < len(W):
        print("No pattern")
        return
    m = 0
    i = 0
    start = 0
    n_comparisons = 0
    while m < len(S):
        n_comparisons += 1
        if S[m] == W[i]:
            if i == len(W) - 1:
                res += 1
                i = 0
                start += 1
                m = start
                continue
            else:
                i += 1
        else:
            i = 0
            start = m + 1
        m += 1
    t_stop = time.perf_counter()
    print(f"{res};{n_comparisons}")


def hash(word, N):
    hw = 0
    d = 256
    q = 101
    for i in range(N):  # N - length of pattern
        hw = (hw * d + ord(word[i])) % q
    if hw < 0:
        hw += q
    return hw


def rabin_karp(path: str, W: str) -> None:
    t_start = time.perf_counter()

    N = len(W)
    h = 1
    d = 256
    q = 101

    for i in range(N - 1):
        h = (h * d) % q

    with open(path, encoding='utf-8') as f:
        text = f.readlines()
    S = ' '.join(text).lower()

    res = 0
    n_comparisons = 0

    if len(S) < N:
        print("No pattern")
        return

    hW = hash(W, N)
    m = 0
    diff_seq = 0

    hS = -1
    while m < len(S) - N + 1:
        n_comparisons += 1
        hS = hash(S, N) if m == 0 else (d * (hS - ord(S[m - 1]) * h) + ord(S[m - 1 + N])) % q
        if hS == hW:
            if S[m:m+N] == W:
                res += 1
            else:
                diff_seq += 1

        m += 1

    t_stop = time.perf_counter()
    print(f"{res};{n_comparisons};{diff_seq}")


def kmp_table(W: str) -> List[int]:
    pos = 1
    cnd = 0
    T = [-1 for _ in range(len(W) + 1)]
    while pos < len(W):
        if W[pos] == W[cnd]:
            T[pos] = T[cnd]
        else:
            T[pos] = cnd
            while cnd >= 0 and W[pos] != W[cnd]:
                cnd = T[cnd]
            pos += 1
            cnd += 1
    T[pos] = cnd
    return T


def KMP(path: str, W: str) -> None:
    t_start = time.perf_counter()
    with open(path, encoding='utf-8') as f:
        text = f.readlines()
    S = ' '.join(text).lower()
    res = 0
    if len(S) < len(W):
        print("No pattern")
        return
    m = 0
    i = 0
    n_comparisons = 0
    T = kmp_table(W)
    while m < len(S):
        n_comparisons += 1
        if S[m] == W[i]:
            m += 1
            i += 1
            if i == len(W):
                res += 1
                i = T[i]
        else:
            i = T[i]
            if i < 0:
                m += 1
                i += 1
    t_stop = time.perf_counter()
    # print("Czas obliczeń:", "{:.7f}".format(t_stop - t_start))
    print(f"{res};{n_comparisons};{T}")


def main():
    root_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(root_dir, 'lotr.txt')

    W = "time."

    regex_naive(file_path, W)
    rabin_karp(file_path, W)
    KMP(file_path, W)


if __name__ == '__main__':
    main()
