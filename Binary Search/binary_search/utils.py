# utils.py

import random


def generate_sorted_list(size=20, min_val=0, max_val=100):
    lst = sorted(random.sample(range(min_val, max_val), size))
    return lst
