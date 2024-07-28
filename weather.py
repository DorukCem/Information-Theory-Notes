import collections
from enum import Enum
import math
import random


class Weather(Enum):
    Excellent = 0b00
    Good = 0b01
    Bad = 0b10
    Terrible = 0b11


MESSAGE_LENGTH = 2
MESSAGE_COUNT = 4

# The probability of each weather condition appering
frequencies = {
    Weather.Excellent: 0.25,
    Weather.Good: 0.25,
    Weather.Bad: 0.25,
    Weather.Terrible: 0.25,
}

# The probabilty that a code will be corrupted given a weather
corruption_odds = {
    Weather.Excellent: 0.01,
    Weather.Good: 0.04,
    Weather.Bad: 0.23,
    Weather.Terrible: 0.43,
}


class Source:
    def __init__(self, num_messages):
        self.messages = random.choices(
            list(frequencies.keys()), list(frequencies.values()), k=num_messages
        )

    def _flip_random_bit(number):
        return Weather(number.value ^ 1 << random.randint(0, MESSAGE_LENGTH - 1))

    def _corrupt_message(message):
        if random.uniform(0, 1) < corruption_odds[message]:
            return Source._flip_random_bit(message)
        return message

    def _send_message(message, reciever):
        message = Source._corrupt_message(message)
        reciever.recieve_message(message)

    def send_all(self, reciever):
        for weather in self.messages:
            Source._send_message(weather, reciever)


class Reciever:
    def __init__(self):
        self.messages = []

    def recieve_message(self, message):
        self.messages.append(message)


def print_messages(sender, reciever):
    for a, b in zip(sender.messages, reciever.messages):
        print(a.value, b.value, end="\n")


def calcualte_entropy(probabilties):
    return -sum(map(lambda p: p * math.log2(p), probabilties))


def calculate_frequencies(messages):
    counter = collections.Counter(messages)
    num_messages = len(messages)
    freqs = {k: v / num_messages for k, v in counter.items()}
    return freqs


def construct_joint_prob_dist_table(frequencies, corruption_odds):
    table = [[0 for _ in frequencies.keys()] for _ in frequencies.keys()]
    for i, (k, v) in enumerate(frequencies.items()):
        p_fail = v * corruption_odds[k] * 1 / (MESSAGE_COUNT - 1)
        p_success = v * (1 - corruption_odds[k])
        table[i] = [p_fail for _ in table[i]]
        table[i][i] = p_success
    
    return table

def print_table(table):
    col_names = [f"     X{n}" for n in range(len(table))] + ["     P(X)"]
    print(*col_names)
    print("-------"*6)
    for i, row in enumerate(table):
        truncated = [format(num, '.5f') for num in row]
        row_name = f"Y{i}  |"
        print(row_name, *truncated, format(sum(row), '.5f'))
    sum_cols =  [ format(sum(x), '.5f') for x in zip(*table) ]
    print("P(Y)|", *sum_cols)
    

if __name__ == "__main__":
    sender = Source(100)
    reciever = Reciever()
    sender.send_all(reciever)

    # input_entropy = calcualte_entropy(frequencies.values())
    # print(f"input entropy: {input_entropy}")

    # output_freq = calculate_frequencies(reciever.messages)
    # print(f"output frequencies: {output_freq}")

    table = construct_joint_prob_dist_table(frequencies, corruption_odds)
    print_table(table)