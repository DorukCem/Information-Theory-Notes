from enum import Enum
import random


class Weather(Enum):
    Excellent = 0b00
    Good = 0b01
    Bad = 0b10
    Terrible = 0b11

MESSAGE_LENGTH = 2

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
    def __init__(self):
        self.weathers = random.choices(
            list(frequencies.keys()), list(frequencies.values()), k=100
        )

    def _flip_random_bit(number):
        Weather(number.value ^ 1 << random.randint(0, MESSAGE_LENGTH-1)) 

    def _corrupt_message(message):
        if random.uniform(0, 1) < corruption_odds[message]:
            return Source._flip_random_bit(message)
        return message

    def _send_message(message, reciever):
        message = Source._corrupt_message(message)
        reciever.recieve_message(message)

    def send_all(self, reciever):
        for weather in self.weathers:
            Source._send_message(weather, reciever)


class Reciever:
    def __init__(self):
        self.messages = []

    def recieve_message(self, message):
        self.messages.append(message)


if __name__ == "__main__":
    sender = Source()
    reciever = Reciever()
    sender.send_all(reciever)
    for msg in reciever.messages[:10]:
        print(msg)
