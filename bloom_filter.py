import math
from typing import List, Tuple, Dict
import time
import os


def hash(word: str, N: int, q: int) -> int:
    hw = 0
    d = 256
    for i in range(N):
        hw = (hw * d + ord(word[i])) % q
    return hw


def RK_bloom(path: str, sub_str: List[str], N: int) -> Tuple[Dict[str, int], int]:
    start = time.perf_counter()
    with open(path, encoding='utf-8') as f:
        text = f.readlines()
    S = ' '.join(text).lower()

    P = 0.001
    n = 20
    b = math.ceil((-n * math.log(P)) / (math.log(2) ** 2))
    k = math.ceil((b / n) * math.log(2))
    d = 256
    q1 = 173
    q2 = 211

    sub_str_set = set(sub_str)
    bloom_filter = [0 for _ in range(b)]
    res = {sub: 0 for sub in sub_str}
    fake_pos = 0

    h1 = 1
    h2 = 1
    for i in range(N - 1):
        h1 = (h1 * d) % q1
        h2 = (h2 * d) % q2

    for sub in sub_str:
        for i in range(k):
            N = len(sub)
            hW = (hash(sub, N, q1) + i * hash(sub, N, q2)) % b
            bloom_filter[hW] = 1

    hash1 = hash(S, N, q1)
    hash2 = hash(S, N, q2)
    for m in range(len(S) - N):
        wasZero = False
        for i in range(k):
            curr_hash = (hash1 + i * hash2) % b
            if bloom_filter[curr_hash] == 0:
                wasZero = True
                break
        if not wasZero:
            if S[m:m + N] in sub_str_set:
                res[S[m:m + N]] += 1
            else:
                fake_pos += 1
        hash1 = (d * (hash1 - ord(S[m]) * h1) + ord(S[m + N])) % q1
        hash2 = (d * (hash2 - ord(S[m]) * h2) + ord(S[m + N])) % q2
        if hash1 < 0:
            hash1 += q1
        if hash2 < 0:
            hash2 += q2
    end = time.perf_counter()
    print(f"{end - start}")
    return res, fake_pos


def main():
    root_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(root_dir, 'lotr.txt')

    sub_str = ['gandalf', 'looking', 'blocked', 'comment', 'pouring', 'finally', 'hundred',
               'hobbits', 'however', 'popular', 'nothing', 'enjoyed', 'stuffed', 'relaxed',
               'himself', 'present', 'deliver', 'welcome', 'baggins', 'further']

    res, fake_pos = RK_bloom(file_path, sub_str, len(sub_str[0]))
    i = 0
    sum_occ = 0
    for sub, occ in res.items():
        if i == len(res) - 1:
            print(f"{sub} - {occ}", end=". ")
        else:
            print(f"{sub} - {occ}", end=", ")
        if i != 0 and i % 5 == 0:
            print()
        sum_occ += occ
        i += 1
    print(f"\n\nFake positive: {fake_pos}; sum of all pattern occurrences: {sum_occ}.")


if __name__ == '__main__':
    main()
