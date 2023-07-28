import os
import json
from itertools import combinations
import math
import csv

def get_orders(target_path):
    orders = []

    for filename in os.listdir(target_path):
        file_path = os.path.join(target_path, filename)
        if os.path.isfile(file_path):
            with open(file_path, "r") as file:
                content = file.read()
                parsed = json.loads(content)
                order = parsed["testOrder"]
                orders.append(order)
    num_orders = len(orders)
    print("Number of orders:", num_orders)
    return orders

def get_seq(order, t):
    return list(combinations(order, t))

def count_unique_seq(order_list, t):
    seq_list = [get_seq(order, t) for order in order_list]

    unique_subsequences = set(seq for sublist in seq_list for seq in sublist)

    return len(unique_subsequences)


def max_cover_order(orders, selected_orders, t):
    max_cover = 0
    max_order = None
    for order in orders:
        if order not in selected_orders:
            temp_orders = selected_orders + [order]
            temp_cover = count_unique_seq(temp_orders, t)
            cover = count_unique_seq(selected_orders + [order], t)
            #print(f"Temp coverage after adding {order}: {temp_cover}")
            #print(f"Cover after adding {order}: {cover}")
            if cover > max_cover:
                max_cover = cover
                max_order = order
    return max_order


def sort_orders(orders, t):
    total_possibilities = math.factorial(len(orders[0])) / math.factorial(len(orders[0]) - t) # total possibilities
    #print(f"Total possibilities with permutations: {total_possibilities}")
    sorted_orders = [orders[0]]  # start with the first order
    orders.remove(orders[0])
    #print(f"{sorted_orders[0]} - {count_unique_seq(sorted_orders, t) / total_possibilities * 100:.2f}% coverage")
    while orders:
        next_order = max_cover_order(orders, sorted_orders, t)
        sorted_orders.append(next_order)
        orders.remove(next_order)
        #print(f"{next_order} - {min(count_unique_seq(sorted_orders, t) / total_possibilities * 100, 100):.2f}% coverage")
    return sorted_orders

def get_victims_or_brittle(github_slug, module,target_path_polluter_cleaner):
    output = []
    with open(target_path_polluter_cleaner, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            module_name = row['module'].split('/')[-1] if row['module'] != '.' else ''
            if row['github_slug'] == github_slug and module_name == module:
                if row['type_victim_or_brittle'] == 'victim':
                    output.append([row['polluter/state-setter'], row['victim/brittle'], row['potential_cleaner'],1])
                    output.append([row['polluter/state-setter'], row['potential_cleaner'], row['victim/brittle'],2])
                elif row['type_victim_or_brittle'] == 'brittle':
                    output.append([row['polluter/state-setter'], row['victim/brittle'],3])
                    output.append([row['victim/brittle'], row['polluter/state-setter'],4])
    return output

def find_OD_in_sorted_orders(sorted_orders, OD_list):
    OD_found = set()
    sorted_order_count = 0

    for order in sorted_orders:
        sorted_order_count += 1

        i = 0
        while i < len(OD_list):
            OD = OD_list[i]
            if all(elem in order for elem in OD[:-1]) and all(order.index(OD[j]) <= order.index(OD[j + 1]) for j in range(len(OD) - 2)):
                OD_found.add(tuple(OD))

                # Check the last element in the OD and pop the relevant elements from OD_list
                last_element = OD[-1]
                if last_element == 1:
                    OD_list = [od for od in OD_list if od[1] != OD[1]]
                elif last_element == 2:
                    OD_list = [od for od in OD_list if od[2] != OD[2]]
                elif last_element == 3:
                    OD_list = [od for od in OD_list if od[1] != OD[1]]
                elif last_element == 4:
                    OD_list = [od for od in OD_list if od[0] != OD[0]]
            else:
                i += 1

        if len(OD_list) == 0:
            return sorted_order_count, OD_found, OD_list

    #print(f"Number of OD not found: {len(OD_list)}")
    return sorted_order_count, OD_found, OD_list


if __name__ == "__main__":
    github_slug = input("Enter the github slug: ")
    module = input("Enter the module name (or press Enter to match any): ")
    target_path_polluter_cleaner = input("Please enter the target path for polluter cleaner list: ")
    result = get_victims_or_brittle(github_slug, module,target_path_polluter_cleaner)
    #print(f"Number OD pairs found: {len(result)}")
    target_path = input("Please enter the target path for generated orders: ")
    orders = get_orders(target_path)
    t = int(input("Please enter the value of t: "))
    #print("Sorted Orders: ")
    sorted_orders = sort_orders(orders, t)

    sorted_order_count, OD_found, not_found_ODs = find_OD_in_sorted_orders(sorted_orders, result)
    print(f"Number of sorted orders needed to find all OD: {sorted_order_count}")
    #print("OD found: ", OD_found)
    #print("OD not found: ", not_found_ODs)