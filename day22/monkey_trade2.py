#! /usr/bin/env python3


from typing import Dict, Sequence


def mix(number, secret_number):
    return number ^ secret_number


def prune(number):
    return number % 16777216


def next_number(secret_number):
    secret_number = prune(mix(secret_number * 64, secret_number))
    secret_number = prune(mix(secret_number // 32, secret_number))
    secret_number = prune(mix(secret_number * 2048, secret_number))
    return secret_number


def calc_number_sequence(secret_num, iterations):
    sequence = [secret_num % 10]
    for _ in range(iterations):
        secret_num = next_number(secret_num)
        sequence.append(secret_num % 10)
    return sequence


def calc_price_dict(buyer_sequences):
    price_dict = {}
    # print(len(buyer_sequences))
    for seq in buyer_sequences:
        already_used = set()
        # print(len(seq))
        for ii in range(4, len(seq)):
            four_diffs = (seq[ii-3] - seq[ii-4],
                          seq[ii-2] - seq[ii-3],
                          seq[ii-1] - seq[ii-2],
                          seq[ii]   - seq[ii-1])
            price = seq[ii]
            if four_diffs not in already_used:
                if four_diffs in price_dict:
                    price_dict[four_diffs] += price
                else:
                    price_dict[four_diffs] = price
                already_used.add(four_diffs)

    # print(len(price_dict))
    return price_dict


def main():
    data = open("input.txt", "r")
    initial_numbers = []
    for line in data:
        initial_numbers.append(int(line))
    # initial_numbers = [123]
    # print(initial_numbers)
    buyer_sequences = []
    for initial_num in initial_numbers:
        buyer_sequences.append(calc_number_sequence(initial_num, 2000))
    
    # for _ in initial_numbers:
    #     print(buyer_sequences)

    # print(sum(final_numbers))

    # keys: 4 diff sequence
    # values: total number of bananas earned
    price_dict = calc_price_dict(buyer_sequences)

    print(max(price_dict.values()))


if __name__ == "__main__":
    main()
