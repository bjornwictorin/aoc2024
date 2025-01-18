#! /usr/bin/env python3


def mix(number, secret_number):
    return number ^ secret_number


def prune(number):
    return number % 16777216


def next_number(secret_number):
    secret_number = prune(mix(secret_number * 64, secret_number))
    secret_number = prune(mix(secret_number // 32, secret_number))
    secret_number = prune(mix(secret_number * 2048, secret_number))
    return secret_number


def calc_number(secret_num, iterations):
    for _ in range(iterations):
        secret_num = next_number(secret_num)
    return secret_num


def main():
    data = open("input.txt", "r")
    initial_numbers = []
    for line in data:
        initial_numbers.append(int(line))
    # print(initial_numbers)
    final_numbers = []
    for initial_num in initial_numbers:
        final_numbers.append(calc_number(initial_num, 2000))
    
    # print(final_numbers)
    print(sum(final_numbers))


if __name__ == "__main__":
    main()
