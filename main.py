import random
import warnings
import matplotlib.pyplot as plt
import pandas as pd

warnings.filterwarnings('ignore')

six_star_rate = 0.015
everything_else_rate = 1 - six_star_rate
rising_rate = 0.025

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
    old_six_star_rate = weights[1]
    new_six_star_rate = old_six_star_rate + adjustment
    new_else_rate = weights[0] - adjustment
    weights[0] = new_else_rate
    weights[1] = new_six_star_rate

def multi_roll():
    character_pool = generate_character_pool()
    weights = generate_weights()
    roll_results = []
    i = 1
    while i < 71:
        if i >= 60:
            adjust_weights(weights, rising_rate)
        if i == 70:
            roll_results.append(character_pool[1])
            break
        roll_result = single_roll(character_pool, weights)
        if roll_result == [character_pool[1]]:
            roll_results.append(roll_result)
            break
        else:
            roll_results.append(roll_result)
        i += 1
    return roll_results

def main():
    cycles = int(input("How many pull cycles? "))
    pull_totals = []
    for i in range(0, cycles):
        pull_totals.append(len(multi_roll()))

    plt.figure()
    df = pd.DataFrame(pull_totals, columns=['Pull'])
    df = df.sort_values(by='Pull')
    df.Pull.value_counts()[df.Pull.unique()].plot(kind='bar', title='REVERSE: 1999 | Pulls Required to Acquire a 6*')
    plt.ylabel('Occurences')
    plt.xlabel('Pull #')
    plt.show()

main()