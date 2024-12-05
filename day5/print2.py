#!/usr/bin/env python3

def swap(update, page_pos, other_page_pos):
    tmp = update[page_pos]
    update[page_pos] = update[other_page_pos]
    update[other_page_pos] = tmp


def main():
    input_data = open("input.txt", "r")
    middle_pages = []
    ordering_rules = []
    updates = []
    for line in input_data:
        if "|" in line:
            ordering_rules.append(tuple(line.rstrip().split("|")))
        elif "," in line:
            updates.append(line.rstrip().split(","))
    # print(ordering_rules)
    # print(updates)

    for update in updates:
        approved = True
        num_pages = len(update)
        for page_pos in range(num_pages):
            for other_page_pos in range(num_pages):
                if page_pos < other_page_pos and (update[page_pos], update[other_page_pos]) not in ordering_rules:
                    approved = False
                    swap(update, page_pos, other_page_pos)
                elif page_pos > other_page_pos and (update[other_page_pos], update[page_pos]) not in ordering_rules:
                    approved = False
                    swap(update, page_pos, other_page_pos)
        if not approved:
            middle_pages.append(int(update[num_pages//2]))

    print(middle_pages)
    print(sum(middle_pages))

if __name__ == "__main__":
    main()
