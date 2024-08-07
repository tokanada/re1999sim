import random
import warnings
import matplotlib.pyplot as plt
import pandas as pd
from multiprocessing import Pool, freeze_support

warnings.filterwarnings('ignore')

six_star_rate = 0.006
everything_else_rate = 1 - six_star_rate

def generate_character_pool():
    character_pool = ["Everything else", "Six Star"]
    return character_pool


def generate_weights():
    weights = [everything_else_rate, six_star_rate]
    return weights


def single_roll(character_pool, weights):
    roll = random.choices(character_pool, weights=weights)
    return roll


def adjust_weights(weights, adjustment):
    new_six_star_rate = adjustment
    new_else_rate = weights[0] - adjustment
    weights[0] = new_else_rate
    weights[1] = new_six_star_rate


def do_loop():
    roll_results = 0
    character_pool = generate_character_pool()
    weights = generate_weights()
    i = 1
    while i < 91:
        if i == 75:
            adjust_weights(weights, 0.3238)
        if i == 90:
            roll_results = i
            break
        roll_result = single_roll(character_pool, weights)
        if roll_result == [character_pool[1]]:
            roll_results = i
            break
        i += 1
    return roll_results


def multi_roll(cycles, processes):
    iterations = list(range(0, cycles))

    with Pool(processes=processes) as pool:
        results = pool.starmap(do_loop, [() for i in iterations])

    return results


def main():
    cycles = int(input("How many pull cycles? "))
    processes = int(input("How many threads to run? "))
    pull_totals = multi_roll(cycles, processes)

    plt.figure()
    df = pd.DataFrame(pull_totals, columns=['Pull'])
    df = df.sort_values(by='Pull')
    df.Pull.value_counts()[df.Pull.unique()].plot(kind='bar', title='Genshin Impact | Pulls Required to Acquire a 5*')
    plt.ylabel('Occurences')
    plt.xlabel('Pull #')
    plt.show()


if __name__ == "__main__":
    freeze_support()
    main()
