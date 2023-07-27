import os
import json
from itertools import combinations
import math


def get_orders():
    target_path = "/Users/satvikeltepu/Desktop/code/generate_orders_java/outputs/inter/Activiti/Activiti/activiti-spring-boot-starter/b11f757"
    orders = []

    for filename in os.listdir(target_path):
        file_path = os.path.join(target_path, filename)
        if os.path.isfile(file_path):
            with open(file_path, "r") as file:
                content = file.read()
                parsed = json.loads(content)
                order = parsed["testOrder"]
                orders.append(order)

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
            print(f"Temp coverage after adding {order}: {temp_cover}")
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
    print(f"{sorted_orders[0]} - {count_unique_seq(sorted_orders, t) / total_possibilities * 100:.2f}% coverage")
    while orders:
        next_order = max_cover_order(orders, sorted_orders, t)
        sorted_orders.append(next_order)
        orders.remove(next_order)
        print(f"{next_order} - {min(count_unique_seq(sorted_orders, t) / total_possibilities * 100, 100):.2f}% coverage")
    return sorted_orders

if __name__ == "__main__":
    orders = get_orders()
    sort_orders(orders, 2)
    
